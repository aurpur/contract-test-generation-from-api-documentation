# 🔄 Flux de Workflow Complet et Détaillé

## Vue d'Ensemble

Le système est un framework multi-agent pour la génération automatique de tests contractuels à partir de documentation API (Bruno Collections). Le workflow comprend 5 phases principales avec intégration TestFixer et boucle de rétroaction.

---

## 📊 Architecture Globale

```
┌─────────────────────────────────────────────────────────────────┐
│                         MAIN ORCHESTRATOR                        │
│                      (src/main.py)                              │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
        ┌───────────────────────────────────────────┐
        │          SHARED CONTEXT MANAGER            │
        │  (Mémoire partagée entre tous les agents)  │
        │   - Endpoints Contexts                     │
        │   - Oracles                                │
        │   - Generated Tests                        │
        │   - Execution Results                      │
        └───────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
        ┏━━━━━━━━━━┓   ┏━━━━━━━━━━━┓   ┏━━━━━━━━━┓
        ┃ ORACLE   ┃   ┃ CONTRACTOR ┃   ┃ RUNNER  ┃
        ┃  AGENT   ┃   ┃   AGENT    ┃   ┃  AGENT  ┃
        ┗━━━━━━━━━━┛   ┗━━━━━━━━━━━┛   ┗━━━━━━━━━┛
             │               │               │
             │               │               ├─────┐
             │               │               │     │
             │               │               ▼     ▼
             │               │          ┌─────────────┐
             │               │          │  TESTFIXER  │
             │               │          │  (Sub-Agent)│
             │               │          └─────────────┘
             │               │
             └───────────────┴───────────────┘
                         EVENT BUS
              (Communication pub/sub entre agents)
```

---

## 🔄 Phase 1 : Parsing de la Collection Bruno

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1 : BRUNO COLLECTION PARSING                         │
└─────────────────────────────────────────────────────────────┘

INPUT: Bruno Collection JSON (bruno_collections/example_api/Sample_API_Collection.json)

    📄 main.py
     │
     ├─► 1.1 Lecture du fichier JSON
     │
     ├─► 1.2 BrunoParser.parse_collection()
     │    │
     │    ├─► Extraction des endpoints
     │    ├─► Parsing des requêtes HTTP
     │    ├─► Extraction des headers
     │    ├─► Parsing du body (JSON/XML)
     │    ├─► Extraction des scripts de test
     │    └─► Identification du type d'auth
     │
     └─► 1.3 Création des EndpointContext
          │
          └─► Stockage dans ContextManager
               │
               └─► Pour chaque endpoint:
                    - endpoint_id (UUID)
                    - name, path, method
                    - auth_type, headers
                    - request_body, response_schema
                    - bruno_tests (scripts originaux)

OUTPUT: Liste d'EndpointContext stockés en mémoire

Métriques:
  - endpoints_parsed: Nombre d'endpoints identifiés
  - total_endpoints: Nombre total d'endpoints
```

---

## 🔮 Phase 2 : Génération des Oracles

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2 : ORACLE GENERATION (LLM-Powered)                 │
└─────────────────────────────────────────────────────────────┘

    📨 Event: "oracle.generate_oracles"
     │
     ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃               ORACLE AGENT                              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
     │
     ├─► 2.1 Pour chaque EndpointContext:
     │    │
     │    ├─► Récupération du contexte
     │    │    - Endpoint path, method, parameters
     │    │    - Bruno test scripts
     │    │    - Response schema
     │    │
     │    ├─► 2.2 Construction du prompt LLM
     │    │    ┌────────────────────────────────────┐
     │    │    │  PROMPT TEMPLATE:                  │
     │    │    │  - "Analyze API endpoint..."       │
     │    │    │  - Endpoint details                │
     │    │    │  - Bruno test scripts              │
     │    │    │  - "Generate assertions..."        │
     │    │    └────────────────────────────────────┘
     │    │
     │    ├─► 2.3 Appel LLM (Ollama/OpenAI/Anthropic)
     │    │    │
     │    │    └─► Response contient:
     │    │         - HTTP status code expected
     │    │         - JSONPath assertions
     │    │         - Business rules
     │    │         - Test description
     │    │
     │    ├─► 2.4 Parsing de la réponse LLM
     │    │    │
     │    │    └─► Extraction:
     │    │         - status_code
     │    │         - assertions[]
     │    │         - business_rules[]
     │    │
     │    └─► 2.5 Création Oracle
     │         │
     │         └─► Stockage dans ContextManager
     │              - oracle_id (UUID)
     │              - endpoint_id (référence)
     │              - expected_status_code
     │              - assertions (JSONPath + expected value)
     │              - business_rules
     │              - confidence_score
     │
     └─► 2.6 Publication de l'événement
          │
          └─► Event: "oracle.oracles_generated"
               └─► Payload: {oracle_ids: [...]}

OUTPUT: Liste d'Oracles avec assertions JSONPath

Métriques:
  - oracles_generated: Nombre d'oracles créés
  - llm_calls: Nombre d'appels LLM
  - avg_confidence: Score de confiance moyen
```

---

## 🏗️ Phase 3 : Génération du Code de Test

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 3 : TEST CODE GENERATION (Template-Based)           │
└─────────────────────────────────────────────────────────────┘

    📨 Event: "contractor.generate_tests"
     │
     ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃             CONTRACTOR AGENT                            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
     │
     ├─► 3.1 Pour chaque Oracle:
     │    │
     │    ├─► Récupération Oracle + EndpointContext
     │    │
     │    ├─► 3.2 Construction des variables template
     │    │    ┌────────────────────────────────────┐
     │    │    │  TEMPLATE VARIABLES:               │
     │    │    │  - test_class_name                 │
     │    │    │  - endpoint_path                   │
     │    │    │  - http_method                     │
     │    │    │  - base_url                        │
     │    │    │  - auth_config                     │
     │    │    │  - headers                         │
     │    │    │  - request_body                    │
     │    │    │  - status_code_assertion           │
     │    │    │  - jsonpath_assertions[]           │
     │    │    │  - business_rules (comments)       │
     │    │    └────────────────────────────────────┘
     │    │
     │    ├─► 3.3 Rendu Jinja2 Template
     │    │    │
     │    │    └─► Template: rest_assured_test.java.j2
     │    │         │
     │    │         ├─► Authentication block
     │    │         │    - Basic Auth
     │    │         │    - Bearer Token
     │    │         │    - API Key
     │    │         │
     │    │         ├─► Request configuration
     │    │         │    - Headers
     │    │         │    - Body
     │    │         │    - Content-Type
     │    │         │
     │    │         ├─► HTTP call
     │    │         │    - .get(), .post(), .put(), .delete()
     │    │         │
     │    │         └─► Assertions
     │    │              - .statusCode(200)
     │    │              - .body("path.to.field", equalTo(value))
     │    │              - JSONPath validations
     │    │
     │    ├─► 3.4 Formatage du code Java
     │    │    │
     │    │    └─► Code formatting (indentation, imports)
     │    │
     │    └─► 3.5 Création GeneratedTest
     │         │
     │         └─► Stockage dans ContextManager
     │              - test_id (UUID)
     │              - oracle_id (référence)
     │              - test_class_name
     │              - test_code (Java)
     │              - file_path
     │              - package_name
     │
     ├─► 3.6 Génération pom.xml
     │    │
     │    └─► Template: pom.xml.j2
     │         - Dependencies (rest-assured, junit)
     │         - Maven plugins
     │         - Java version (11)
     │
     ├─► 3.7 Écriture des fichiers sur disque
     │    │
     │    ├─► output/exec_YYYYMMDD_HHMMSS/tests/
     │    │    └─► com/example/tests/TestXXX.java
     │    │
     │    └─► output/exec_YYYYMMDD_HHMMSS/pom.xml
     │
     └─► 3.8 Publication de l'événement
          │
          └─► Event: "contractor.tests_generated"
               └─► Payload: {test_ids: [...]}

OUTPUT: Fichiers Java + pom.xml sur disque

Métriques:
  - tests_generated: Nombre de tests générés
  - lines_of_code: Total lignes de code
  - assertions_count: Nombre d'assertions
  - pom_generated: 1 si pom.xml créé
```

---

## 🧪 Phase 4 : Exécution et Correction des Tests

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 4 : TEST EXECUTION + COMPILATION FIX + TESTFIXER    │
└─────────────────────────────────────────────────────────────┘

    📨 Event: "runner.execute_tests"
     │
     ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                 RUNNER AGENT                            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
     │
     ├─► 4.1 Récupération des tests depuis ContextManager
     │
     ├─► 4.2 Écriture des tests sur disque
     │    │
     │    └─► Fichiers .java dans output/exec_*/tests/
     │
     │
     ├─► 🔨 4.3 COMPILATION DU CODE GÉNÉRÉ
     │    │
     │    └─► _compile_and_fix_generated_code()
     │         │
     │         ├─► Tentative 1/3: mvn compile
     │         │    │
     │         │    ├─► ✅ SUCCESS → Passe à 4.4
     │         │    │
     │         │    └─► ❌ COMPILATION ERROR
     │         │         │
     │         │         └─► Parsing des erreurs Maven
     │         │              │
     │         │              ├─► Regex: \[ERROR\] (.+\.java):\[(\d+),(\d+)\] (.+)
     │         │              │
     │         │              └─► Pour chaque erreur:
     │         │                   │
     │         │                   ├─► Lecture du fichier .java
     │         │                   │
     │         │                   ├─► Appel TestFixer
     │         │                   │    │
     │         │                   │    └─► TestFixer.analyze_and_fix_generated_code()
     │         │                   │         │
     │         │                   │         ├─► Catégorisation: GENERATED_CODE_ERROR
     │         │                   │         │
     │         │                   │         ├─► Construction prompt LLM
     │         │                   │         │    ┌──────────────────────────────┐
     │         │                   │         │    │ PROMPT:                      │
     │         │                   │         │    │ "Fix compilation error..."   │
     │         │                   │         │    │ - Original code              │
     │         │                   │         │    │ - Error message              │
     │         │                   │         │    │ - File type (Java)           │
     │         │                   │         │    │ - Instructions spécifiques   │
     │         │                   │         │    └──────────────────────────────┘
     │         │                   │         │
     │         │                   │         ├─► Appel LLM (60s timeout)
     │         │                   │         │
     │         │                   │         ├─► Extraction du code corrigé
     │         │                   │         │
     │         │                   │         └─► Retour code fixé
     │         │                   │
     │         │                   └─► Écriture du code corrigé
     │         │
     │         ├─► Tentative 2/3: mvn compile (après fixes)
     │         │
     │         └─► Tentative 3/3: mvn compile (si encore erreurs)
     │
     │
     ├─► ▶️ 4.4 EXÉCUTION DES TESTS MAVEN
     │    │
     │    └─► mvn test -Dtest=TestClass1,TestClass2,...
     │         │
     │         ├─► Timeout: 300s par défaut
     │         │
     │         └─► Capture stdout/stderr
     │
     │
     ├─► 📊 4.5 PARSING DES RÉSULTATS JUNIT XML
     │    │
     │    └─► Lecture target/surefire-reports/TEST-*.xml
     │         │
     │         └─► Pour chaque test:
     │              │
     │              ├─► ✅ PASSED
     │              │    └─► TestExecutionResult(passed=True)
     │              │
     │              └─► ❌ FAILED
     │                   │
     │                   └─► TestExecutionResult(
     │                        │   passed=False,
     │                        │   error_message=...,
     │                        │   assertion_failures=[...],
     │                        │   retry_count=0
     │                        └─► )
     │
     │
     ├─► 🔧 4.6 AUTO-FIX DES TESTS ÉCHOUÉS (TestFixer)
     │    │
     │    └─► _try_auto_fix_tests()
     │         │
     │         └─► Pour chaque test échoué:
     │              │
     │              ├─► Récupération du test depuis ContextManager
     │              │
     │              ├─► 🔍 TestFixer.analyze_and_fix_test()
     │              │    │
     │              │    ├─► Catégorisation de l'erreur
     │              │    │    │
     │              │    │    ├─► ASSERTION: AssertionError
     │              │    │    ├─► COMPILATION: Cannot find symbol
     │              │    │    ├─► RUNTIME: NullPointerException
     │              │    │    ├─► TIMEOUT: Test timeout
     │              │    │    ├─► NETWORK: Connection refused
     │              │    │    ├─► AUTH: 401 Unauthorized
     │              │    │    ├─► DATA: JSON parsing error
     │              │    │    └─► UNKNOWN: Autres erreurs
     │              │    │
     │              │    ├─► Tentatives de correction (max 2 par catégorie)
     │              │    │    │
     │              │    │    └─► Pour chaque tentative:
     │              │    │         │
     │              │    │         ├─► Construction prompt spécialisé
     │              │    │         │    ┌──────────────────────────────┐
     │              │    │         │    │ CATEGORY-SPECIFIC PROMPT:    │
     │              │    │         │    │ - Error type                 │
     │              │    │         │    │ - Test code                  │
     │              │    │         │    │ - Error message              │
     │              │    │         │    │ - Fix suggestions            │
     │              │    │         │    │ - Best practices             │
     │              │    │         │    └──────────────────────────────┘
     │              │    │         │
     │              │    │         ├─► Appel LLM (60s timeout)
     │              │    │         │
     │              │    │         ├─► Extraction code corrigé
     │              │    │         │
     │              │    │         └─► Validation syntaxique
     │              │    │
     │              │    └─► Retour code corrigé ou None
     │              │
     │              ├─► Si code corrigé:
     │              │    │
     │              │    ├─► Mise à jour du test dans ContextManager
     │              │    │
     │              │    ├─► Écriture sur disque
     │              │    │
     │              │    ├─► Ré-exécution du test
     │              │    │    └─► mvn test -Dtest=TestClass
     │              │    │
     │              │    └─► Analyse du résultat:
     │              │         │
     │              │         ├─► ✅ PASSED → Test corrigé avec succès
     │              │         │    └─► Métrique: tests_auto_fixed++
     │              │         │
     │              │         └─► ❌ STILL FAILED → Test toujours en échec
     │              │
     │              └─► Si aucun fix ou toujours en échec:
     │                   └─► Ajout à la liste des tests non corrigés
     │
     │
     ├─► 🔄 4.7 DÉCLENCHEMENT DE LA RÉGÉNÉRATION
     │    │
     │    └─► _trigger_regeneration()
     │         │
     │         └─► Pour chaque test toujours en échec:
     │              │
     │              ├─► Vérification retry_count < max_retries (3)
     │              │
     │              ├─► ✅ Peut régénérer:
     │              │    │
     │              │    └─► Publication événement
     │              │         │
     │              │         └─► Event: "contractor.regenerate_test"
     │              │              │
     │              │              └─► Payload: {
     │              │                   test_id,
     │              │                   failure_reason,
     │              │                   assertion_failures,
     │              │                   retry_count++,
     │              │                   session_id
     │              │                 }
     │              │
     │              └─► ❌ Max retries atteint:
     │                   └─► Test définitivement échoué
     │
     │
     ├─► 4.8 Stockage des résultats
     │    │
     │    └─► ContextManager.add_execution_result()
     │         └─► Pour chaque test:
     │              - test_id
     │              - passed (True/False)
     │              - execution_time
     │              - error_message
     │              - assertion_failures[]
     │              - retry_count
     │
     │
     └─► 4.9 Publication de l'événement
          │
          └─► Event: "runner.tests_executed"
               └─► Payload: {
                    session_id,
                    passed: X,
                    failed: Y,
                    auto_fixed: Z
                  }

OUTPUT: Résultats d'exécution + Tests corrigés automatiquement

Métriques:
  - tests_executed: Nombre de tests exécutés
  - tests_passed: Nombre de tests réussis
  - tests_failed: Nombre de tests échoués
  - tests_auto_fixed: Nombre de tests corrigés par TestFixer
  - generated_code_fixed: Nombre de fichiers compilés corrigés
  - retries: Nombre de régénérations déclenchées
```

---

## 🔄 Phase 5 : Régénération et Boucle de Rétroaction

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 5 : TEST REGENERATION LOOP (Feedback Loop)          │
└─────────────────────────────────────────────────────────────┘

    📨 Event: "contractor.regenerate_test"
     │
     ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃             CONTRACTOR AGENT                            ┃
┃           (Regeneration Handler)                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
     │
     ├─► 5.1 Réception de l'événement
     │    │
     │    └─► _handle_regenerate_test_event()
     │         │
     │         └─► Création Task(task_type="regenerate_test")
     │
     │
     ├─► 5.2 Régénération du test
     │    │
     │    └─► _regenerate_failed_test()
     │         │
     │         ├─► Récupération du test original
     │         │    └─► ContextManager.get_test(test_id)
     │         │
     │         ├─► Récupération de l'oracle associé
     │         │    └─► ContextManager.get_oracle(oracle_id)
     │         │
     │         ├─► Récupération du contexte endpoint
     │         │    └─► ContextManager.get_endpoint_context(context_id)
     │         │
     │         ├─► ♻️ Génération du nouveau code
     │         │    │
     │         │    └─► _generate_test_from_oracle()
     │         │         │
     │         │         ├─► Même processus que Phase 3
     │         │         │    (mais avec contexte d'échec)
     │         │         │
     │         │         └─► Nouveau code Java généré
     │         │
     │         ├─► Mise à jour du test
     │         │    │
     │         │    └─► ContextManager.update_test()
     │         │         │
     │         │         └─► Garde même test_id
     │         │              Nouveau test_code
     │         │              Incrémente retry_count
     │         │
     │         └─► Métrique: tests_regenerated++
     │
     │
     ├─► 5.3 Exécution automatique du test régénéré
     │    │
     │    └─► Publication événement
     │         │
     │         └─► Event: "runner.execute_tests"
     │              │
     │              └─► Payload: {
     │                   test_ids: [test_id],
     │                   session_id
     │                 }
     │
     │
     └─► 5.4 Retour à la Phase 4
          │
          └─► Le test régénéré passe par:
               │
               ├─► 4.3 Compilation + fix si nécessaire
               ├─► 4.4 Exécution Maven
               ├─► 4.5 Parsing résultats
               ├─► 4.6 TestFixer si échec
               │
               └─► Si encore échec et retry_count < max_retries:
                    │
                    └─► Retour Phase 5 (nouvelle régénération)

                   Si retry_count >= max_retries:
                    │
                    └─► Test définitivement échoué
                         (enregistré dans les rapports finaux)

Boucle de rétroaction:
  Test Failed → TestFixer (2 tentatives) → Still Failed? → Regenerate → Execute → TestFixer → ...
  
Condition d'arrêt:
  - Test passed ✅
  - OU retry_count >= max_retries (3) ❌
```

---

## 🎯 TestFixer - Sous-Système Détaillé

```
┌─────────────────────────────────────────────────────────────┐
│           TESTFIXER SUB-AGENT (LLM-Powered)                │
│        (Intégré dans Runner, appelé automatiquement)        │
└─────────────────────────────────────────────────────────────┘

DEUX MODES D'OPÉRATION:

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  MODE 1: FIX GENERATED CODE (Compilation Errors)        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
     │
     └─► analyze_and_fix_generated_code()
          │
          ├─► INPUT:
          │    - code: Code Java original
          │    - error_message: Erreur de compilation Maven
          │    - file_name: Nom du fichier
          │    - file_type: "Java"
          │    - iteration: Numéro de tentative
          │
          ├─► PROCESS:
          │    │
          │    ├─► Catégorisation: GENERATED_CODE_ERROR
          │    │
          │    ├─► Construction prompt spécialisé
          │    │    ┌──────────────────────────────────────┐
          │    │    │ PROMPT FOR GENERATED CODE:           │
          │    │    │                                      │
          │    │    │ "You are a code fixing expert..."   │
          │    │    │ "Fix the following compilation      │
          │    │    │  error in generated Java code"      │
          │    │    │                                      │
          │    │    │ Original Code:                       │
          │    │    │ ```java                              │
          │    │    │ [code]                               │
          │    │    │ ```                                  │
          │    │    │                                      │
          │    │    │ Compilation Error:                   │
          │    │    │ [error_message]                      │
          │    │    │                                      │
          │    │    │ File: [file_name]                    │
          │    │    │ Type: [file_type]                    │
          │    │    │                                      │
          │    │    │ Instructions:                        │
          │    │    │ - Fix compilation error              │
          │    │    │ - Keep Rest-Assured syntax           │
          │    │    │ - Preserve test logic                │
          │    │    │ - Add missing imports                │
          │    │    │ - Return ONLY fixed code             │
          │    │    └──────────────────────────────────────┘
          │    │
          │    ├─► Appel LLM (60s timeout, temperature=0.2)
          │    │
          │    ├─► Extraction du code corrigé
          │    │    └─► Regex: ```java\n(.*?)```
          │    │
          │    └─► Validation: code non vide
          │
          └─► OUTPUT:
               - Code Java corrigé (ou None si échec)
               - Métrique: generated_code_fixed++


┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  MODE 2: FIX TEST FAILURES (Runtime/Assertion Errors)   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
     │
     └─► analyze_and_fix_test()
          │
          ├─► INPUT:
          │    - test_code: Code du test
          │    - error_message: Message d'erreur d'exécution
          │    - test_name: Nom de la classe de test
          │    - iteration: Numéro de tentative
          │
          ├─► PROCESS:
          │    │
          │    ├─► 1. Catégorisation de l'erreur
          │    │    │
          │    │    ├─► ASSERTION (expected X but was Y)
          │    │    ├─► COMPILATION (cannot find symbol)
          │    │    ├─► RUNTIME (NullPointerException)
          │    │    ├─► TIMEOUT (test timed out)
          │    │    ├─► NETWORK (Connection refused)
          │    │    ├─► AUTH (401 Unauthorized)
          │    │    ├─► DATA (JSON parse error)
          │    │    └─► UNKNOWN (autres)
          │    │
          │    ├─► 2. Tentatives de correction (max 2 par catégorie)
          │    │    │
          │    │    └─► Pour chaque tentative:
          │    │         │
          │    │         ├─► Vérification des limites
          │    │         │    └─► fixes_by_category[ASSERTION] < 2
          │    │         │
          │    │         ├─► Construction prompt par catégorie
          │    │         │    │
          │    │         │    ├─► ASSERTION:
          │    │         │    │    "Fix assertion mismatches..."
          │    │         │    │    "Check JSONPath expressions..."
          │    │         │    │
          │    │         │    ├─► COMPILATION:
          │    │         │    │    "Fix missing imports..."
          │    │         │    │    "Check method signatures..."
          │    │         │    │
          │    │         │    ├─► RUNTIME:
          │    │         │    │    "Add null checks..."
          │    │         │    │    "Handle exceptions..."
          │    │         │    │
          │    │         │    ├─► TIMEOUT:
          │    │         │    │    "Increase timeout values..."
          │    │         │    │    "Optimize test execution..."
          │    │         │    │
          │    │         │    ├─► NETWORK:
          │    │         │    │    "Check endpoint URL..."
          │    │         │    │    "Add retry logic..."
          │    │         │    │
          │    │         │    ├─► AUTH:
          │    │         │    │    "Verify credentials..."
          │    │         │    │    "Check auth headers..."
          │    │         │    │
          │    │         │    └─► DATA:
          │    │         │         "Fix JSON structure..."
          │    │         │         "Handle optional fields..."
          │    │         │
          │    │         ├─► Appel LLM (60s timeout)
          │    │         │
          │    │         ├─► Extraction code corrigé
          │    │         │
          │    │         ├─► Si code valide:
          │    │         │    └─► fixes_by_category[category]++
          │    │         │         return fixed_code
          │    │         │
          │    │         └─► Si échec:
          │    │              └─► Tentative suivante
          │    │
          │    └─► Si toutes tentatives échouent:
          │         └─► return None (test sera régénéré)
          │
          └─► OUTPUT:
               - Code de test corrigé (ou None)
               - Métriques:
                 - test_fixed++
                 - fixes_by_category[category]++


STATISTIQUES TESTFIXER:

    get_statistics() retourne:
    {
        "test_fixed": 5,              # Tests d'exécution corrigés
        "generated_code_fixed": 2,    # Fichiers compilés corrigés
        "fixes_by_category": {
            "assertion": 3,
            "compilation": 1,
            "runtime": 1,
            "generated_code_error": 2
        }
    }
```

---

## 📁 Structure des Outputs

```
output/
└── exec_YYYYMMDD_HHMMSS/          # Session d'exécution
    │
    ├── contexts/                   # EndpointContexts (JSON)
    │   └── context_<uuid>.json
    │
    ├── oracles/                    # Oracles générés (JSON)
    │   └── oracle_<uuid>.json
    │
    ├── tests/                      # Code Java généré
    │   └── com/
    │       └── example/
    │           └── tests/
    │               ├── GetUsersTest.java
    │               ├── CreateUserTest.java
    │               └── ...
    │
    ├── pom.xml                     # Maven configuration
    │
    ├── logs/                       # Logs détaillés
    │   ├── main.log
    │   ├── oracle_agent.log
    │   ├── contractor_agent.log
    │   └── runner_agent.log
    │
    ├── reports/                    # Rapports d'exécution
    │   ├── execution_summary.json
    │   ├── test_results.json
    │   └── metrics.json
    │
    ├── traces/                     # Traces LLM
    │   ├── oracle_trace_<uuid>.json
    │   └── testfixer_trace_<uuid>.json
    │
    └── graphs/                     # Visualisations
        ├── test_results.html
        └── confidence_distribution.html
```

---

## 🔄 Event Bus - Communication Inter-Agents

```
┌─────────────────────────────────────────────────────────────┐
│                     EVENT BUS (Pub/Sub)                     │
└─────────────────────────────────────────────────────────────┘

ÉVÉNEMENTS PUBLIÉS:

1. oracle.generate_oracles
   ├─► Publisher: Main Orchestrator
   ├─► Subscriber: Oracle Agent
   └─► Payload: {session_id, endpoint_contexts[]}

2. oracle.oracles_generated
   ├─► Publisher: Oracle Agent
   ├─► Subscriber: Main Orchestrator
   └─► Payload: {session_id, oracle_ids[]}

3. contractor.generate_tests
   ├─► Publisher: Main Orchestrator
   ├─► Subscriber: Contractor Agent
   └─► Payload: {session_id, oracle_ids[]}

4. contractor.tests_generated
   ├─► Publisher: Contractor Agent
   ├─► Subscriber: Main Orchestrator
   └─► Payload: {session_id, test_ids[]}

5. runner.execute_tests
   ├─► Publisher: Main Orchestrator / Contractor (régénération)
   ├─► Subscriber: Runner Agent
   └─► Payload: {session_id, test_ids[]}

6. runner.tests_executed
   ├─► Publisher: Runner Agent
   ├─► Subscriber: Main Orchestrator
   └─► Payload: {session_id, passed, failed, auto_fixed}

7. contractor.regenerate_test
   ├─► Publisher: Runner Agent
   ├─► Subscriber: Contractor Agent
   └─► Payload: {test_id, failure_reason, retry_count, session_id}


SYNCHRONISATION:

    Main Orchestrator utilise asyncio.Event pour synchroniser:
    
    oracle_done = asyncio.Event()
    contractor_done = asyncio.Event()
    runner_done = asyncio.Event()
    
    Phase 1 → Phase 2 → oracle_done.wait()
    Phase 2 → Phase 3 → contractor_done.wait()
    Phase 3 → Phase 4 → runner_done.wait()
```

---

## 🎯 Métriques Globales

```
FINAL METRICS:
{
    "session_id": "uuid",
    "timestamp": "2025-12-01T04:00:00",
    "duration_seconds": 45.2,
    
    "parsing": {
        "endpoints_parsed": 5,
        "total_endpoints": 5
    },
    
    "oracle_agent": {
        "oracles_generated": 5,
        "llm_calls": 5,
        "avg_confidence": 0.85,
        "duration_seconds": 12.3
    },
    
    "contractor_agent": {
        "tests_generated": 5,
        "tests_regenerated": 2,
        "lines_of_code": 450,
        "assertions_count": 25,
        "pom_generated": 1,
        "duration_seconds": 8.7
    },
    
    "runner_agent": {
        "tests_executed": 7,          # 5 initiaux + 2 régénérés
        "tests_passed": 6,
        "tests_failed": 1,
        "tests_auto_fixed": 3,
        "generated_code_fixed": 1,
        "retries": 2,
        "duration_seconds": 24.2
    },
    
    "testfixer": {
        "test_fixed": 3,
        "generated_code_fixed": 1,
        "fixes_by_category": {
            "assertion": 2,
            "compilation": 0,
            "runtime": 1,
            "generated_code_error": 1
        }
    },
    
    "final_results": {
        "total_tests": 5,
        "passed": 4,
        "failed": 1,
        "success_rate": 0.80
    }
}
```

---

## 🔀 Diagramme de Flux Simplifié

```
START
  │
  ├─► [1] Parse Bruno Collection
  │    └─► EndpointContexts → ContextManager
  │
  ├─► [2] Oracle Agent (LLM)
  │    └─► Oracles → ContextManager
  │
  ├─► [3] Contractor Agent
  │    └─► Java Tests → Disk + ContextManager
  │
  ├─► [4] Runner Agent
  │    │
  │    ├─► 🔨 Compile Code
  │    │    └─► Fix compilation errors (TestFixer)
  │    │
  │    ├─► ▶️ Execute Tests (Maven)
  │    │
  │    ├─► 🔧 Auto-Fix Failed Tests (TestFixer)
  │    │    └─► Re-execute fixed tests
  │    │
  │    └─► 🔄 Trigger Regeneration (if still failing)
  │
  ├─► [5] Regeneration Loop
  │    │
  │    ├─► Contractor regenerates test
  │    │
  │    └─► Back to [4] (Execute + Fix)
  │         │
  │         └─► Loop until: PASSED or MAX_RETRIES
  │
  └─► END
       │
       └─► Generate Reports + Metrics
```

---

## 🚀 Commande d'Exécution

```bash
python src/main.py bruno_collections/example_api/Sample_API_Collection.json
```

---

## 📚 Technologies et Frameworks

- **Language**: Python 3.9+
- **Async**: asyncio
- **LLM**: Ollama (llama3.2), OpenAI, Anthropic
- **Templates**: Jinja2
- **Tests**: Java + Rest-Assured + JUnit 5
- **Build**: Maven
- **Parsing**: XML (JUnit), JSON (Bruno)
- **Logging**: Loguru
- **Context**: In-memory shared state (ContextManager)

---

## ✨ Points Clés

1. **Architecture Multi-Agent**: 3 agents autonomes (Oracle, Contractor, Runner) + 1 sub-agent (TestFixer)

2. **Communication Async**: Event Bus pub/sub pour découplage

3. **TestFixer Intelligent**: 
   - Fixe les erreurs de compilation du code généré (AVANT exécution)
   - Fixe les erreurs d'exécution des tests (APRÈS exécution)
   - 8 catégories d'erreurs reconnues
   - Max 2 tentatives par catégorie

4. **Boucle de Rétroaction**: Test échoué → TestFixer → Encore échoué? → Régénération → Ré-exécution

5. **LLM-Powered**: Oracles + TestFixer utilisent des LLMs pour génération/correction

6. **Contexte Partagé**: Tous les agents partagent le même ContextManager (en mémoire)

7. **Traçabilité**: Tous les artéfacts sauvegardés (contexts, oracles, tests, logs, traces)

---

**Auteur**: Aurel IKAMA HONEY  
**Date**: 1er Décembre 2025  
**Version**: Phase 5 - TestFixer Intégré
