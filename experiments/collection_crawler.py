"""
===============================================================================
Collection Crawler for Public APIs
===============================================================================

OBJECTIF:
    Ce module parcourt les APIs publiques et génère des collections Bruno
    au format approprié pour les expérimentations.

FONCTIONNALITÉS:
    - Crawling d'APIs publiques (JSONPlaceholder, HTTPBin, etc.)
    - Génération de fichiers .bru conformes au format Bruno
    - Extraction de métadonnées pour chaque endpoint
    - Support des différents types de requêtes HTTP

USAGE:
    python -m experiments.collection_crawler

Auteur: Aurel IKAMA HONEY
Date: December 12, 2025
===============================================================================
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class CollectionCrawler:
    """
    Crawls public APIs and generates Bruno collections.
    """
    
    def __init__(self, output_dir: Path = Path("bruno_collections")):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _create_bruno_item(
        self,
        name: str,
        method: str,
        url: str,
        docs: str = "",
        headers: Optional[List[Dict]] = None,
        params: Optional[List[Dict]] = None,
        body_mode: str = "none",
        body_json: Optional[str] = None,
        seq: int = 1
    ) -> Dict:
        """Create a Bruno collection item in proper format."""
        return {
            "type": "http",
            "name": name,
            "filename": f"{name}.bru",
            "seq": seq,
            "settings": {},
            "tags": [],
            "examples": [],
            "request": {
                "url": url,
                "method": method,
                "headers": headers or [],
                "params": params or [],
                "body": {
                    "mode": body_mode,
                    "json": body_json,
                    "formUrlEncoded": [],
                    "multipartForm": [],
                    "file": []
                },
                "script": {},
                "vars": {},
                "assertions": [],
                "tests": "",
                "docs": docs,
                "auth": {"mode": "none"}
            }
        }
    
    def _create_bruno_collection(
        self,
        name: str,
        items: List[Dict],
        version: str = "1"
    ) -> Dict:
        """Create a complete Bruno collection."""
        return {
            "name": name,
            "version": version,
            "items": items,
            "environments": [],
            "root": {
                "request": {
                    "auth": {"mode": "none"}
                }
            },
            "brunoConfig": {
                "version": version,
                "name": name,
                "type": "collection",
                "ignore": ["node_modules", ".git"],
                "size": 0.0,
                "filesCount": len(items)
            }
        }
    
    def crawl_jsonplaceholder(self) -> Path:
        """Crawl JSONPlaceholder API and generate Bruno collection."""
        print("\n🌐 Crawling JSONPlaceholder API...")
        
        base_url = "https://jsonplaceholder.typicode.com"
        items = []
        seq = 1
        
        # Define resources
        resources = [
            ("posts", "Blog posts", "post"),
            ("comments", "Post comments", "comment"),
            ("albums", "Photo albums", "album"),
            ("photos", "Photos", "photo"),
            ("todos", "Todo items", "todo"),
            ("users", "Users", "user")
        ]
        
        for resource, description, singular in resources:
            # GET all
            items.append(self._create_bruno_item(
                name=f"Get all {resource}",
                method="GET",
                url=f"{base_url}/{resource}",
                docs=f"Retrieve all {description}",
                seq=seq
            ))
            seq += 1
            
            # GET by ID
            items.append(self._create_bruno_item(
                name=f"Get {singular} by ID",
                method="GET",
                url=f"{base_url}/{resource}/{{id}}",
                docs=f"Retrieve a single {singular} by ID",
                seq=seq
            ))
            seq += 1
            
            # POST create
            sample_body = self._get_jsonplaceholder_sample_body(resource)
            items.append(self._create_bruno_item(
                name=f"Create {singular}",
                method="POST",
                url=f"{base_url}/{resource}",
                docs=f"Create a new {singular}",
                body_mode="json",
                body_json=json.dumps(sample_body, indent=2),
                seq=seq
            ))
            seq += 1
            
            # PUT update
            items.append(self._create_bruno_item(
                name=f"Update {singular}",
                method="PUT",
                url=f"{base_url}/{resource}/{{id}}",
                docs=f"Update an existing {singular}",
                body_mode="json",
                body_json=json.dumps(sample_body, indent=2),
                seq=seq
            ))
            seq += 1
            
            # DELETE
            items.append(self._create_bruno_item(
                name=f"Delete {singular}",
                method="DELETE",
                url=f"{base_url}/{resource}/{{id}}",
                docs=f"Delete a {singular}",
                seq=seq
            ))
            seq += 1
        
        # Create collection
        collection = self._create_bruno_collection(
            name="JSONPlaceholder REST API",
            items=items
        )
        
        # Save collection
        output_path = self.output_dir / "jsonplaceholder"
        output_path.mkdir(parents=True, exist_ok=True)
        collection_file = output_path / "collection.json"
        
        with open(collection_file, 'w') as f:
            json.dump(collection, f, indent=2)
        
        print(f"✅ Created collection: {collection['name']}")
        print(f"   Endpoints: {len(items)}")
        print(f"   Location: {collection_file}")
        
        return collection_file
    
    def _get_jsonplaceholder_sample_body(self, resource: str) -> Dict:
        """Get sample request body for JSONPlaceholder resource."""
        samples = {
            "posts": {"title": "Sample Post", "body": "This is a sample post", "userId": 1},
            "comments": {"postId": 1, "name": "Sample Comment", "email": "user@example.com", "body": "Comment text"},
            "albums": {"title": "Sample Album", "userId": 1},
            "photos": {"albumId": 1, "title": "Sample Photo", "url": "https://via.placeholder.com/600/92c952", "thumbnailUrl": "https://via.placeholder.com/150/92c952"},
            "todos": {"title": "Sample Todo", "completed": False, "userId": 1},
            "users": {"name": "John Doe", "username": "johndoe", "email": "john@example.com"}
        }
        return samples.get(resource, {})
    
    def crawl_reqres(self) -> Path:
        """Crawl ReqRes API and generate Bruno collection."""
        print("\n🌐 Crawling ReqRes API...")
        
        base_url = "https://reqres.in/api"
        items = []
        seq = 1
        
        # List users
        items.append(self._create_bruno_item(
            name="List users",
            method="GET",
            url=f"{base_url}/users",
            docs="Get paginated list of users",
            params=[
                {"name": "page", "value": "1", "enabled": True},
                {"name": "per_page", "value": "6", "enabled": True}
            ],
            seq=seq
        ))
        seq += 1
        
        # Get single user
        items.append(self._create_bruno_item(
            name="Get single user",
            method="GET",
            url=f"{base_url}/users/{{id}}",
            docs="Get a single user by ID",
            seq=seq
        ))
        seq += 1
        
        # Create user
        user_body = {"name": "John Doe", "job": "Developer"}
        items.append(self._create_bruno_item(
            name="Create user",
            method="POST",
            url=f"{base_url}/users",
            docs="Create a new user",
            body_mode="json",
            body_json=json.dumps(user_body, indent=2),
            seq=seq
        ))
        seq += 1
        
        # Update user
        items.append(self._create_bruno_item(
            name="Update user",
            method="PUT",
            url=f"{base_url}/users/{{id}}",
            docs="Update an existing user",
            body_mode="json",
            body_json=json.dumps(user_body, indent=2),
            seq=seq
        ))
        seq += 1
        
        # Delete user
        items.append(self._create_bruno_item(
            name="Delete user",
            method="DELETE",
            url=f"{base_url}/users/{{id}}",
            docs="Delete a user",
            seq=seq
        ))
        seq += 1
        
        # Register
        register_body = {"email": "eve.holt@reqres.in", "password": "pistol"}
        items.append(self._create_bruno_item(
            name="Register user",
            method="POST",
            url=f"{base_url}/register",
            docs="Register a new user",
            body_mode="json",
            body_json=json.dumps(register_body, indent=2),
            seq=seq
        ))
        seq += 1
        
        # Login
        login_body = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
        items.append(self._create_bruno_item(
            name="Login",
            method="POST",
            url=f"{base_url}/login",
            docs="Login with credentials",
            body_mode="json",
            body_json=json.dumps(login_body, indent=2),
            seq=seq
        ))
        seq += 1
        
        # Create collection
        collection = self._create_bruno_collection(
            name="ReqRes Users API",
            items=items
        )
        
        # Save collection
        output_path = self.output_dir / "reqres"
        output_path.mkdir(parents=True, exist_ok=True)
        collection_file = output_path / "collection.json"
        
        with open(collection_file, 'w') as f:
            json.dump(collection, f, indent=2)
        
        print(f"✅ Created collection: {collection['name']}")
        print(f"   Endpoints: {len(items)}")
        print(f"   Location: {collection_file}")
        
        return collection_file
    
    def crawl_httpbin(self) -> Path:
        """Crawl HTTPBin API and generate Bruno collection."""
        print("\n🌐 Crawling HTTPBin API...")
        
        base_url = "https://httpbin.org"
        items = []
        seq = 1
        
        # GET request
        items.append(self._create_bruno_item(
            name="GET request",
            method="GET",
            url=f"{base_url}/get",
            docs="Test GET request with query parameters",
            params=[
                {"name": "param1", "value": "value1", "enabled": True},
                {"name": "param2", "value": "value2", "enabled": True}
            ],
            seq=seq
        ))
        seq += 1
        
        # POST request
        post_body = {"key": "value", "test": "data"}
        items.append(self._create_bruno_item(
            name="POST request",
            method="POST",
            url=f"{base_url}/post",
            docs="Test POST request with JSON body",
            body_mode="json",
            body_json=json.dumps(post_body, indent=2),
            seq=seq
        ))
        seq += 1
        
        # Status codes
        for status in [200, 400, 404, 500]:
            items.append(self._create_bruno_item(
                name=f"Status {status}",
                method="GET",
                url=f"{base_url}/status/{status}",
                docs=f"Return status code {status}",
                seq=seq
            ))
            seq += 1
        
        # Headers
        items.append(self._create_bruno_item(
            name="Get headers",
            method="GET",
            url=f"{base_url}/headers",
            docs="Return request headers",
            seq=seq
        ))
        seq += 1
        
        # Delay
        items.append(self._create_bruno_item(
            name="Delayed response",
            method="GET",
            url=f"{base_url}/delay/2",
            docs="Delayed response by 2 seconds",
            seq=seq
        ))
        seq += 1
        
        # Basic auth
        items.append(self._create_bruno_item(
            name="Basic authentication",
            method="GET",
            url=f"{base_url}/basic-auth/user/pass",
            docs="Test basic authentication",
            seq=seq
        ))
        seq += 1
        
        # Create collection
        collection = self._create_bruno_collection(
            name="HTTPBin Testing API",
            items=items
        )
        
        # Save collection
        output_path = self.output_dir / "httpbin"
        output_path.mkdir(parents=True, exist_ok=True)
        collection_file = output_path / "collection.json"
        
        with open(collection_file, 'w') as f:
            json.dump(collection, f, indent=2)
        
        print(f"✅ Created collection: {collection['name']}")
        print(f"   Endpoints: {len(items)}")
        print(f"   Location: {collection_file}")
        
        return collection_file
    
    def crawl_all_public_apis(self) -> List[Path]:
        """Crawl all supported public APIs."""
        print("\n" + "="*70)
        print("                 CRAWLING PUBLIC APIS")
        print("="*70)
        
        collections = []
        
        try:
            collections.append(self.crawl_jsonplaceholder())
        except Exception as e:
            print(f"❌ Failed to crawl JSONPlaceholder: {e}")
        
        try:
            collections.append(self.crawl_reqres())
        except Exception as e:
            print(f"❌ Failed to crawl ReqRes: {e}")
        
        try:
            collections.append(self.crawl_httpbin())
        except Exception as e:
            print(f"❌ Failed to crawl HTTPBin: {e}")
        
        print("\n" + "="*70)
        print(f"✅ Successfully created {len(collections)} collections")
        print("="*70)
        
        return collections


if __name__ == "__main__":
    crawler = CollectionCrawler()
    collections = crawler.crawl_all_public_apis()
    print(f"\n✅ Generated {len(collections)} Bruno collections")
