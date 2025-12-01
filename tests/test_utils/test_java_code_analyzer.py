"""
Unit tests for JavaCodeAnalyzer.

Author: Aurel IKAMA HONEY
"""
import pytest
from utils.java_code_analyzer import JavaCodeAnalyzer, JavaCodeSmell, analyze_java_code


class TestJavaCodeAnalyzer:
    """Test suite for JavaCodeAnalyzer."""
    
    def test_initialization(self):
        """Test analyzer initialization."""
        analyzer = JavaCodeAnalyzer()
        assert analyzer.smells == []
    
    def test_detect_magic_numbers(self):
        """Test magic number detection."""
        code = """
        public void testMethod() {
            int timeout = 3000;
            double rate = 0.15;
            int port = 8080;
        }
        """
        
        analyzer = JavaCodeAnalyzer()
        result = analyzer.analyze(code)
        
        assert result["summary"]["total_smells"] > 0
        assert "magic_numbers" in result["by_type"]
    
    def test_detect_long_methods(self):
        """Test long method detection."""
        # Create a method with 60 lines
        lines = ["public void longMethod() {"]
        lines.extend([f"    int var{i} = {i};" for i in range(60)])
        lines.append("}")
        code = "\n".join(lines)
        
        analyzer = JavaCodeAnalyzer()
        result = analyzer.analyze(code)
        
        assert any(smell["type"] == "long_method" for smell in analyzer.smells)
    
    def test_detect_empty_catch_block(self):
        """Test empty catch block detection."""
        code = """
        public void testMethod() {
            try {
                riskyOperation();
            } catch (Exception e) {
            }
        }
        """
        
        analyzer = JavaCodeAnalyzer()
        result = analyzer.analyze(code)
        
        critical_smells = result["critical"]
        assert len(critical_smells) > 0
        assert any("empty_catch_block" in str(smell) for smell in critical_smells)
    
    def test_detect_deep_nesting(self):
        """Test deep nesting detection."""
        code = """
        public void testMethod() {
            if (condition1) {
                if (condition2) {
                    if (condition3) {
                        if (condition4) {
                            if (condition5) {
                                doSomething();
                            }
                        }
                    }
                }
            }
        }
        """
        
        analyzer = JavaCodeAnalyzer()
        result = analyzer.analyze(code)
        
        assert any(smell["type"] == "deep_nesting" for smell in analyzer.smells)
    
    def test_detect_long_parameter_list(self):
        """Test long parameter list detection."""
        code = """
        public void complexMethod(
            String param1,
            int param2,
            double param3,
            boolean param4,
            Object param5,
            String param6,
            int param7
        ) {
            // method body
        }
        """
        
        analyzer = JavaCodeAnalyzer()
        result = analyzer.analyze(code)
        
        assert any(smell["type"] == "long_parameter_list" for smell in analyzer.smells)
    
    def test_detect_test_smells_eager_test(self):
        """Test eager test smell detection."""
        code = """
        @Test
        public void testEverything() {
            assertEquals(1, service.method1());
            assertEquals(2, service.method2());
            assertEquals(3, service.method3());
            assertEquals(4, service.method4());
            assertEquals(5, service.method5());
            assertEquals(6, service.method6());
            assertEquals(7, service.method7());
            assertEquals(8, service.method8());
            assertEquals(9, service.method9());
            assertEquals(10, service.method10());
            assertEquals(11, service.method11());
        }
        """
        
        analyzer = JavaCodeAnalyzer()
        result = analyzer.analyze(code)
        
        assert any(smell["type"] == "eager_test" for smell in analyzer.smells)
    
    def test_detect_test_smells_sleepy_test(self):
        """Test sleepy test smell detection."""
        code = """
        @Test
        public void testAsync() {
            service.startAsync();
            Thread.sleep(1000);
            assertTrue(service.isCompleted());
        }
        """
        
        analyzer = JavaCodeAnalyzer()
        result = analyzer.analyze(code)
        
        assert any(smell["type"] == "sleepy_test" for smell in analyzer.smells)
    
    def test_detect_hardcoded_credentials(self):
        """Test hardcoded credentials detection."""
        code = """
        public void connectToDb() {
            String password = "mySecretPassword123";
            String apiKey = "sk-1234567890abcdef";
        }
        """
        
        analyzer = JavaCodeAnalyzer()
        result = analyzer.analyze(code)
        
        critical_smells = result["critical"]
        assert any("hard_coding" in str(smell) for smell in critical_smells)
    
    def test_detect_duplicate_code(self):
        """Test duplicate code detection."""
        code = """
        public void method1() {
            System.out.println("This is a long duplicated line of code");
            System.out.println("This is a long duplicated line of code");
            System.out.println("This is a long duplicated line of code");
            System.out.println("This is a long duplicated line of code");
        }
        """
        
        analyzer = JavaCodeAnalyzer()
        result = analyzer.analyze(code)
        
        assert any(smell["type"] == "duplicate_code" for smell in analyzer.smells)
    
    def test_categorize_by_severity(self):
        """Test smell categorization by severity."""
        code = """
        public void problematicMethod() {
            String password = "secret123";  // Critical
            int magic = 12345;              // Medium
            catch (Exception e) {}          // Critical
        }
        """
        
        analyzer = JavaCodeAnalyzer()
        result = analyzer.analyze(code)
        
        assert "critical" in result
        assert "high" in result
        assert "medium" in result
        assert "low" in result
        assert "summary" in result
        
        summary = result["summary"]
        assert "total_smells" in summary
        assert "critical_count" in summary
    
    def test_convenience_function(self):
        """Test convenience analyze_java_code function."""
        code = """
        public void testMethod() {
            int magic = 9999;
        }
        """
        
        result = analyze_java_code(code)
        
        assert "summary" in result
        assert result["summary"]["total_smells"] > 0
    
    def test_no_smells_in_clean_code(self):
        """Test that clean code produces minimal smells."""
        code = """
        public void calculateTotal() {
            int subtotal = calculateSubtotal();
            int tax = calculateTax(subtotal);
            return subtotal + tax;
        }
        
        private int calculateSubtotal() {
            return items.stream()
                .mapToInt(Item::getPrice)
                .sum();
        }
        """
        
        analyzer = JavaCodeAnalyzer()
        result = analyzer.analyze(code)
        
        # Should have very few or no critical/high severity smells
        critical_and_high = len(result["critical"]) + len(result["high"])
        assert critical_and_high == 0


class TestJavaCodeSmell:
    """Test suite for JavaCodeSmell class."""
    
    def test_smell_initialization(self):
        """Test smell object initialization."""
        smell = JavaCodeSmell(
            smell_type="test_smell",
            severity="high",
            description="Test description",
            line_number=42,
            suggestion="Fix this"
        )
        
        assert smell.smell_type == "test_smell"
        assert smell.severity == "high"
        assert smell.line_number == 42
    
    def test_smell_to_dict(self):
        """Test smell to dictionary conversion."""
        smell = JavaCodeSmell(
            smell_type="test_smell",
            severity="medium",
            description="Test",
            line_number=10,
            suggestion="Improve"
        )
        
        smell_dict = smell.to_dict()
        
        assert smell_dict["type"] == "test_smell"
        assert smell_dict["severity"] == "medium"
        assert smell_dict["line_number"] == 10
        assert smell_dict["suggestion"] == "Improve"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
