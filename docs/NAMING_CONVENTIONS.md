# Conventions de Nommage

Ce document définit les règles de nommage utilisées dans le projet de génération de tests de contrat.

## 📋 Table des Matières

1. [Fichiers Java](#fichiers-java)
2. [Fichiers Gherkin](#fichiers-gherkin)
3. [Rapports et Logs](#rapports-et-logs)
4. [Classes et Méthodes](#classes-et-méthodes)
5. [Variables et Constantes](#variables-et-constantes)

---

## 🔤 Fichiers Java

### Convention : **PascalCase** + Suffix `Test`

**Format** : `{EndpointName}Test.java`

**Règles** :
- ✅ Nom d'endpoint converti en PascalCase
- ✅ Suffix `Test` ajouté automatiquement
- ✅ Pas de préfixe de méthode HTTP (évite duplication)
- ✅ Caractères spéciaux supprimés
- ❌ Pas d'espaces, tirets ou underscores

**Exemples** :
```
Endpoint: "Get Users"     → GetUsersTest.java
Endpoint: "create-user"   → CreateUserTest.java
Endpoint: "update_order"  → UpdateOrderTest.java
Endpoint: "delete item"   → DeleteItemTest.java
```

**Implémentation** :
```python
def _generate_class_name(self, context: EndpointContext) -> str:
    # Convert to PascalCase
    name = context.name.replace("-", " ").replace("_", " ")
    name = "".join(word.capitalize() for word in name.split())
    # Remove invalid characters
    name = re.sub(r'[^a-zA-Z0-9]', '', name)
    # Add Test suffix
    return f"{name}Test"
```

---

## 🥒 Fichiers Gherkin

### Convention : **snake_case** + Extension `.feature`

**Format** : `{endpoint_name}.feature`

**Règles** :
- ✅ Nom d'endpoint en minuscules
- ✅ Underscores pour séparer les mots
- ✅ Pas de méthode HTTP dans le nom
- ✅ Caractères spéciaux supprimés
- ❌ Pas d'espaces, tirets ou majuscules

**Exemples** :
```
Endpoint: "Get Users"     → get_users.feature
Endpoint: "create-user"   → create_user.feature
Endpoint: "update_order"  → update_order.feature
Endpoint: "DELETE Item"   → delete_item.feature
```

**Implémentation** :
```python
def _generate_feature_file_name(self, context: EndpointContext) -> str:
    # Normalize: spaces and dashes → underscores
    name = context.name.lower().replace(' ', '_').replace('-', '_')
    # Remove duplicate underscores
    name = re.sub(r'_+', '_', name)
    # Remove invalid characters
    name = re.sub(r'[^a-z0-9_]', '', name)
    return f"{name}.feature"
```

---

## 📊 Rapports et Logs

### Convention : **snake_case** + **timestamp** + Extension

**Format** : `{report_type}_{YYYYMMDD_HHMMSS}.{ext}`

**Types de rapports** :

| Type | Format | Exemple |
|------|--------|---------|
| Agent Execution | `agent_execution_report_{timestamp}.html` | `agent_execution_report_20251120_011813.html` |
| Test Execution | `test_execution_report_{timestamp}.html` | `test_execution_report_20251120_011217.html` |
| Oracle List | `oracle_list_{timestamp}.txt` | `oracle_list_20251120_011217.txt` |
| Execution Trace | `execution_trace_{timestamp}.json` | `execution_trace_20251120_011217.json` |
| Workflow Log | `workflow_log_{timestamp}.log` | `workflow_log_20251120_011217.log` |
| Agent Metrics | `agent_metrics_{timestamp}.png` | `agent_metrics_20251120_011217.png` |
| Test Results | `test_results_{timestamp}.png` | `test_results_20251120_011217.png` |

**Règles** :
- ✅ snake_case pour le type de rapport
- ✅ Timestamp format : YYYYMMDD_HHMMSS
- ✅ Extension appropriée (.html, .txt, .json, .log, .png)
- ❌ Pas d'espaces ou caractères spéciaux

**Implémentation** :
```python
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report_path = self.output_dir / f"agent_execution_report_{timestamp}.html"
graph_path = self.graphs_dir / f"agent_metrics_{timestamp}.png"
trace_path = self.traces_dir / f"execution_trace_{timestamp}.json"
log_path = self.logs_dir / f"workflow_log_{timestamp}.log"
```

---

## 💻 Classes et Méthodes

### Classes Java

**Convention** : **PascalCase**

**Exemples** :
```java
public class GetUsersTest { }
public class CreateUserTest { }
public class UpdateOrderTest { }
```

### Méthodes Java

**Convention** : **camelCase** + Préfixe `test`

**Exemples** :
```java
@Test
public void testGetUsers() { }

@Test
public void testCreateUser() { }

@Test
public void testUpdateOrder() { }
```

**Implémentation** :
```python
def _generate_method_name(self, context: EndpointContext) -> str:
    name = context.name.replace("-", " ").replace("_", " ")
    words = name.split()
    if not words:
        return "testEndpoint"
    return "test" + "".join(word.capitalize() for word in words)
```

### Classes Python

**Convention** : **PascalCase**

**Exemples** :
```python
class BaseAgent:
class ReportGenerator:
class SharedContext:
class EndpointContext:
```

### Méthodes Python

**Convention** : **snake_case**

**Exemples** :
```python
def generate_class_name(self):
def process_task(self, task):
def send_message(self, message):
def _handle_private_method(self):  # méthode privée avec _
```

---

## 🔢 Variables et Constantes

### Variables Python

**Convention** : **snake_case**

**Exemples** :
```python
endpoint_context = EndpointContext(...)
test_result = runner.execute_test()
feature_file_name = "get_users.feature"
class_name = "GetUsersTest"
```

### Constantes Python

**Convention** : **UPPER_SNAKE_CASE**

**Exemples** :
```python
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
API_BASE_URL = "http://localhost:8080"
TEMPLATES_DIR = "templates/"
```

### Variables Java

**Convention** : **camelCase**

**Exemples** :
```java
String baseUrl = "http://localhost:8080";
Response response = given().get("/users");
int statusCode = response.getStatusCode();
String userId = "123";
```

---

## 🎯 Résumé des Conventions

| Contexte | Convention | Exemple |
|----------|-----------|---------|
| Fichiers Java | PascalCase + Test | `GetUsersTest.java` |
| Fichiers Gherkin | snake_case | `get_users.feature` |
| Rapports HTML | snake_case + timestamp | `agent_execution_report_20251120.html` |
| Logs/Traces | snake_case + timestamp | `workflow_log_20251120.log` |
| Graphiques | snake_case + timestamp | `agent_metrics_20251120.png` |
| Classes Java | PascalCase | `GetUsersTest` |
| Méthodes Java | camelCase + test | `testGetUsers()` |
| Classes Python | PascalCase | `BaseAgent` |
| Méthodes Python | snake_case | `generate_test()` |
| Variables Python | snake_case | `endpoint_context` |
| Constantes Python | UPPER_SNAKE_CASE | `MAX_RETRIES` |

---

## ⚠️ Caractères Interdits

### Dans tous les noms de fichiers :
- ❌ Espaces : `Get Users.java` → ✅ `GetUsers.java`
- ❌ Caractères spéciaux : `Test@User#1.java` → ✅ `TestUser1.java`
- ❌ Accents : `créer-utilisateur.feature` → ✅ `creer_utilisateur.feature`

### Caractères autorisés :
- ✅ Lettres : `a-z`, `A-Z`
- ✅ Chiffres : `0-9`
- ✅ Underscores : `_` (dans snake_case uniquement)
- ✅ Points : `.` (extensions de fichiers uniquement)

---

## 🔧 Utilitaires de Nommage

### Fonction de Sanitization

```python
def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    return filename
```

### Normalisation d'Endpoint

```python
def normalize_endpoint_name(name: str, style: str = "snake") -> str:
    """
    Normalize endpoint name to specific style.
    
    Args:
        name: Original name
        style: "snake", "pascal", or "camel"
        
    Returns:
        Normalized name
    """
    # Remove special characters
    name = re.sub(r'[^a-zA-Z0-9\s\-_]', '', name)
    
    if style == "snake":
        name = name.lower().replace(' ', '_').replace('-', '_')
        return re.sub(r'_+', '_', name)
    
    elif style == "pascal":
        name = name.replace('-', ' ').replace('_', ' ')
        return "".join(word.capitalize() for word in name.split())
    
    elif style == "camel":
        name = name.replace('-', ' ').replace('_', ' ')
        words = name.split()
        if not words:
            return "endpoint"
        return words[0].lower() + "".join(w.capitalize() for w in words[1:])
    
    return name
```

---

## 📖 Références

- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)
- [Cucumber Naming Conventions](https://cucumber.io/docs/gherkin/reference/)

---

**Dernière mise à jour** : 20 novembre 2025  
**Auteur** : Aurel IKAMA HONEY  
**Version** : 1.0
