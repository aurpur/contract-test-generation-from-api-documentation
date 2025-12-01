# TestFixer Sub-Agent Documentation

## Overview

The **TestFixer** is an LLM-powered sub-agent that automatically fixes failing tests through iterative corrections. It intelligently categorizes errors and applies targeted fixes using specialized prompts for each error type.

## Features

### 🎯 Multi-Category Error Handling

TestFixer supports 7 error categories:

1. **ASSERTION_MISMATCH**: Expected vs actual value mismatches
2. **COMPILATION_ERROR**: Syntax errors, missing imports, incorrect signatures
3. **NULL_POINTER**: NullPointerException issues
4. **RUNTIME_ERROR**: General runtime exceptions
5. **TIMEOUT**: Test timeout issues
6. **TIMING_DEPENDENT**: Assertions on time-sensitive headers (Date, Age, Expires)
7. **UNKNOWN**: Unclassified errors

### 🔄 Iterative Fixing Strategy

- **Max Iterations**: 3 attempts per test (configurable)
- **Max Fixes Per Category**: 2 fix strategies per error category (configurable)
- **Smart Categorization**: Automatically detects error type from error messages
- **Fallback**: Tests that can't be auto-fixed trigger full regeneration

### 🤖 LLM-Powered Corrections

- Uses specialized prompts for each error category
- Low temperature (0.2) for deterministic fixes
- 60-second timeout per LLM call
- Extracts code from markdown code blocks or plain text

### 📊 Detailed Metrics

TestFixer tracks:
- `fixes_applied`: Total successful fixes
- `tests_fixed`: Number of tests successfully fixed
- `fixes_by_category`: Breakdown by error category
- `failed_fixes_by_category`: Failed fix attempts by category
- `success_rate`: Overall fix success percentage
- `total_attempts`: Total fix attempts made

## Configuration

### agents_config.yaml

```yaml
test_fixer:
  name: "Test Fixer Sub-Agent"
  description: "Automatically fixes failing tests using LLM"
  max_iterations: 3              # Max attempts per test
  max_fixes_per_category: 2      # Max fixes to try per error category
  model: llama3.2                # LLM model to use
  timeout: 60                    # Timeout per LLM call (seconds)
```

## Integration in Workflow

### Execution Flow

```
Tests executed → Failed tests identified
                        ↓
            Error categorization (7 categories)
                        ↓
        ┌──────────────┴──────────────┐
        ↓                             ↓
Category-specific fixes    Multiple attempts per category
   (LLM-powered)              (max 2 attempts)
        ↓                             ↓
   ┌────┴────┐                       
   ↓         ↓                       
Fixed   Still failing                
   ↓         ↓                       
Update   Try next                    
metrics   strategy                   
           ↓                         
   All attempts exhausted?           
           ↓                         
    Yes: Trigger full regeneration   
    No: Return fixed code            
```

### Code Integration

TestFixer is initialized in `Runner` agent:

```python
from agents.test_fixer import TestFixer
from utils.llm_client import LLMClient

# Initialize with LLM client
llm_client = LLMClient(base_url=config.llm.base_url, timeout=60)
self.test_fixer = TestFixer(
    llm_client=llm_client,
    model_name="llama3.2",
    max_iterations=3,
    max_fixes_per_category=2
)
```

Called in `_try_auto_fix_tests()`:

```python
fixed_code = await self.test_fixer.analyze_and_fix_test(
    test_code=test.test_code,
    error_message=failed_result.error_message,
    test_name=test.test_class_name
)
```

## LLM Prompts

### Base Prompt Structure

```
You are a Java test fixing expert. Fix the following Rest-Assured test that is failing.

ERROR CATEGORY: {category}
ATTEMPT NUMBER: {attempt}

FAILING TEST CODE:
```java
{code}
```

ERROR MESSAGE:
{error}

INSTRUCTIONS:
{category-specific instructions}

FIXED CODE:
```

### Category-Specific Instructions

#### ASSERTION_MISMATCH
```
1. Analyze the 'expected' vs 'but was' values in the error
2. Update the assertEquals() calls with the correct expected values
3. Keep the test structure unchanged
4. Return ONLY the fixed Java code, no explanations
```

#### COMPILATION_ERROR
```
1. Fix syntax errors (missing semicolons, brackets, quotes)
2. Add missing imports if needed
3. Correct method signatures
4. Return ONLY the fixed Java code, no explanations
```

#### NULL_POINTER
```
1. Add null checks before accessing response values
2. Use Optional or conditional checks
3. Add assertNotNull() where appropriate
4. Return ONLY the fixed Java code, no explanations
```

#### TIMEOUT
```
1. Increase timeout values (double them)
2. Add .timeout() to Rest-Assured calls
3. Consider using async patterns if needed
4. Return ONLY the fixed Java code, no explanations
```

#### TIMING_DEPENDENT
```
1. Remove assertions on timing-dependent headers (Date, Age, Expires)
2. Remove or relax time-based validations
3. Keep all other assertions intact
4. Return ONLY the fixed Java code, no explanations
```

## Logging

TestFixer uses emoji-enhanced logging for better visibility:

- 🔧 **Analyzing**: Starting fix attempt
- 📊 **Category**: Error category identified
- 🔄 **Attempt**: Fix attempt number
- 🤖 **LLM Call**: Calling LLM for fix
- ✅ **Success**: Fix applied successfully
- ❌ **Failure**: Fix attempt failed
- 🔴 **Max Reached**: All attempts exhausted
- ⚠️ **Warning**: No valid code in LLM response
- ⏱️ **Timeout**: LLM call timed out

### Example Log Output

```
INFO | 🔧 Analyzing test failure (iteration 1/3): GetUsersTest
DEBUG | Error message: expected: <200> but was: <404>...
INFO | 📊 Error category: assertion_mismatch
INFO | 🔄 Fix attempt 1/2 for category assertion_mismatch
DEBUG | 🤖 Calling LLM (llama3.2) for fix...
DEBUG | ✅ LLM returned fixed code (1534 chars)
INFO | ✅ Fix applied successfully (category: assertion_mismatch, attempt: 1)
INFO | ✓ Test auto-fixed successfully: GetUsersTest
```

## Metrics Output

At the end of a session:

```python
{
    "fixes_applied": 15,
    "tests_fixed": 12,
    "fixes_by_category": {
        "assertion_mismatch": 8,
        "compilation_error": 3,
        "null_pointer": 2,
        "timing_dependent": 2
    },
    "failed_fixes_by_category": {
        "runtime_error": 2,
        "unknown": 1
    },
    "success_rate": 83.33,
    "total_attempts": 18
}
```

## Performance Considerations

### LLM Calls
- Each fix attempt = 1 LLM call (max 60s)
- Max LLM calls per test = `max_iterations * max_fixes_per_category` = 6 calls
- Total time per test (worst case) = 6 * 60s = 6 minutes

### Optimization Tips
1. **Reduce max_fixes_per_category** to 1 for faster fixes
2. **Lower max_iterations** to 2 for time-critical workflows
3. **Use faster LLM models** (e.g., llama3.2 vs llama3.1)
4. **Increase LLM timeout** if getting frequent timeouts

## Error Handling

### LLM Failures
- **Timeout**: Returns `None`, moves to next attempt
- **Invalid Response**: Logs warning, moves to next attempt
- **Network Error**: Logs error, moves to next attempt

### All Attempts Exhausted
- Marks test for full regeneration
- Updates `failed_fixes_by_category` metrics
- Logs final failure message

## Best Practices

### When to Use TestFixer
✅ **Good use cases:**
- Assertion value mismatches
- Simple compilation errors
- Null pointer issues
- Timeout adjustments
- Removing timing-dependent assertions

❌ **Poor use cases:**
- Complex logic errors
- API contract changes
- Missing test data
- Infrastructure issues

### Configuration Recommendations

**Fast iteration (development):**
```yaml
max_iterations: 2
max_fixes_per_category: 1
model: llama3.2
```

**Thorough fixing (production):**
```yaml
max_iterations: 3
max_fixes_per_category: 2
model: llama3.2
```

**Maximum attempts (critical fixes):**
```yaml
max_iterations: 5
max_fixes_per_category: 3
model: llama3.2
```

## Future Enhancements

### Planned Features
- [ ] Multi-model consensus for fixes
- [ ] Learning from previous fixes (fix history)
- [ ] Custom fix strategies per project
- [ ] Parallel fix attempts for faster results
- [ ] Fix confidence scoring
- [ ] Integration with mutation testing results

### Potential Improvements
- Cache successful fixes for similar errors
- Add support for more error categories
- Implement fix validation before applying
- Add rollback mechanism for bad fixes

## Troubleshooting

### Issue: TestFixer not fixing tests

**Possible causes:**
1. LLM model not available → Check Ollama status
2. Timeout too low → Increase `timeout` in config
3. Error not categorized → Check logs for "UNKNOWN" category
4. LLM returning invalid code → Check LLM response format

**Solutions:**
```bash
# Check Ollama
ollama list

# Test LLM directly
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Fix this Java code: public class Test { }"
}'

# Increase timeout in config
# agents_config.yaml → test_fixer.timeout: 120
```

### Issue: Too many LLM calls

**Cause:** High values for `max_iterations` and `max_fixes_per_category`

**Solution:** Reduce configuration values:
```yaml
max_iterations: 2          # Down from 3
max_fixes_per_category: 1  # Down from 2
```

### Issue: Fixes not persisting

**Cause:** Test not being updated in context manager

**Solution:** Check `context_manager.update_test()` is called:
```python
test.test_code = fixed_code
await self.context_manager.update_test(test, session_id)
```

## Related Documentation

- [Main README](../README.md) - Project overview
- [Phase 5 Summary](PHASE_5_SUMMARY.md) - TestFixer implementation details
- [Agents Configuration](../config/agents_config.yaml) - Configuration reference
- [Runner Agent](../src/agents/runner.py) - Integration code

## Author

Aurel IKAMA HONEY - December 2025

## License

See [LICENSE](../LICENSE)
