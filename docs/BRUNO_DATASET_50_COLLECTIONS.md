# Dataset Bruno - 50 collections hétérogènes

Ce dataset contient 50 collections Bruno, chacune sous forme de fichiers `.bru` (2 requêtes GET non destructives par collection).

- Dossier dataset: `dataset/bruno_collections_50/`
- Total collections: 50
- Total requêtes `.bru`: 100
- Environnements de test (API key / token): `dataset/bruno_collections_50/{nasa,github,gitlab,stackexchange}/environments/Test.bru`

| # | Collection | Domaine | Auth | Docs | Base URL | Exemples (2) |
|---:|---|---|---|---|---|---|
| 1 | `Open-Meteo` | weather | none | https://open-meteo.com/en/docs | https://api.open-meteo.com/v1 | `https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&hourly=temperature_2m`<br/>`https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&daily=temperature_2m_max,temperature_2m_min` |
| 2 | `MET Norway Locationforecast` | weather | none | https://api.met.no/weatherapi/locationforecast/2.0/documentation | https://api.met.no/weatherapi/locationforecast/2.0 | `https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.91&lon=10.75`<br/>`https://api.met.no/weatherapi/locationforecast/2.0/complete?lat=59.91&lon=10.75` |
| 3 | `Nager.Date` | calendar | none | https://date.nager.at/swagger/index.html | https://date.nager.at/api/v3 | `https://date.nager.at/api/v3/AvailableCountries`<br/>`https://date.nager.at/api/v3/PublicHolidays/2025/FR` |
| 4 | `REST Countries` | geography | none | https://restcountries.com/ | https://restcountries.com/v3.1 | `https://restcountries.com/v3.1/all`<br/>`https://restcountries.com/v3.1/name/france` |
| 5 | `Open Library` | education | none | https://openlibrary.org/developers/api | https://openlibrary.org | `https://openlibrary.org/search.json?q=harry%20potter`<br/>`https://openlibrary.org/api/books?bibkeys=ISBN:9780140328721&format=json&jscmd=data` |
| 6 | `Gutendex Project Gutenberg` | education | none | https://gutendex.com/ | https://gutendex.com | `https://gutendex.com/books`<br/>`https://gutendex.com/books?search=sherlock` |
| 7 | `Cat Facts` | entertainment | none | https://catfact.ninja/ | https://catfact.ninja | `https://catfact.ninja/fact`<br/>`https://catfact.ninja/facts?limit=5` |
| 8 | `Dog CEO` | entertainment | none | https://dog.ceo/dog-api/ | https://dog.ceo/api | `https://dog.ceo/api/breeds/list/all`<br/>`https://dog.ceo/api/breed/hound/images/random` |
| 9 | `PokeAPI` | gaming | none | https://pokeapi.co/docs/v2 | https://pokeapi.co/api/v2 | `https://pokeapi.co/api/v2/pokemon/ditto`<br/>`https://pokeapi.co/api/v2/type/3` |
| 10 | `NASA APIs` | science | optional key (DEMO_KEY) | https://api.nasa.gov/ | https://api.nasa.gov | `https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY`<br/>`https://api.nasa.gov/neo/rest/v1/feed?start_date=2025-12-10&end_date=2025-12-11&api_key=DEMO_KEY` |
| 11 | `SpaceX API` | science | none | https://github.com/r-spacex/SpaceX-API | https://api.spacexdata.com/v4 | `https://api.spacexdata.com/v4/launches/latest`<br/>`https://api.spacexdata.com/v4/rockets` |
| 12 | `USGS Earthquake` | geospatial | none | https://earthquake.usgs.gov/fdsnws/event/1/ | https://earthquake.usgs.gov/fdsnws/event/1 | `https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&limit=5`<br/>`https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson` |
| 13 | `Open Notify` | space | none | http://open-notify.org/Open-Notify-API/ | http://api.open-notify.org | `http://api.open-notify.org/iss-now.json`<br/>`http://api.open-notify.org/astros.json` |
| 14 | `Wikipedia REST API` | knowledge | none | https://www.mediawiki.org/wiki/REST_API | https://en.wikipedia.org/api/rest_v1 | `https://en.wikipedia.org/api/rest_v1/page/summary/Paris`<br/>`https://en.wikipedia.org/api/rest_v1/feed/featured/2025/12/16` |
| 15 | `GitHub REST API` | developer | none (rate-limited) | https://docs.github.com/en/rest | https://api.github.com | `https://api.github.com/users/octocat`<br/>`https://api.github.com/repos/octocat/Hello-World` |
| 16 | `GitLab API` | developer | none (rate-limited) | https://docs.gitlab.com/ee/api/ | https://gitlab.com/api/v4 | `https://gitlab.com/api/v4/projects?search=gitlab&simple=true&per_page=5`<br/>`https://gitlab.com/api/v4/users?username=gitlab` |
| 17 | `StackExchange API` | developer | none (key optional) | https://api.stackexchange.com/docs | https://api.stackexchange.com/2.3 | `https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow&pagesize=5`<br/>`https://api.stackexchange.com/2.3/tags?order=desc&sort=popular&site=stackoverflow&pagesize=5` |
| 18 | `Hacker News API` | media | none | https://github.com/HackerNews/API | https://hacker-news.firebaseio.com/v0 | `https://hacker-news.firebaseio.com/v0/topstories.json`<br/>`https://hacker-news.firebaseio.com/v0/item/8863.json` |
| 19 | `CoinGecko` | finance | none (rate-limited) | https://www.coingecko.com/en/api/documentation | https://api.coingecko.com/api/v3 | `https://api.coingecko.com/api/v3/ping`<br/>`https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd` |
| 20 | `Frankfurter FX` | finance | none | https://www.frankfurter.app/docs/ | https://api.frankfurter.app | `https://api.frankfurter.app/latest?from=EUR`<br/>`https://api.frankfurter.app/2020-01-01..2020-01-31?from=USD&to=EUR` |
| 21 | `Open Brewery DB` | commerce | none | https://www.openbrewerydb.org/documentation | https://api.openbrewerydb.org/v1 | `https://api.openbrewerydb.org/v1/breweries?per_page=5`<br/>`https://api.openbrewerydb.org/v1/breweries/search?query=dog` |
| 22 | `Fake Store API` | commerce | none | https://fakestoreapi.com/docs | https://fakestoreapi.com | `https://fakestoreapi.com/products?limit=5`<br/>`https://fakestoreapi.com/products/1` |
| 23 | `DummyJSON` | commerce | none | https://dummyjson.com/docs | https://dummyjson.com | `https://dummyjson.com/products?limit=5`<br/>`https://dummyjson.com/users?limit=5` |
| 24 | `Mercado Libre` | commerce | none for public endpoints | https://developers.mercadolibre.com.ar/en_us/api-docs-en | https://api.mercadolibre.com | `https://api.mercadolibre.com/sites`<br/>`https://api.mercadolibre.com/sites/MLA/search?q=iphone&limit=5` |
| 25 | `Open Food Facts` | food | none | https://world.openfoodfacts.org/data | https://world.openfoodfacts.org | `https://world.openfoodfacts.org/api/v2/product/737628064502.json`<br/>`https://world.openfoodfacts.org/api/v2/search?categories_tags=en:beverages&page_size=5` |
| 26 | `TheMealDB` | food | none | https://www.themealdb.com/api.php | https://www.themealdb.com/api/json/v1/1 | `https://www.themealdb.com/api/json/v1/1/search.php?s=Arrabiata`<br/>`https://www.themealdb.com/api/json/v1/1/lookup.php?i=52772` |
| 27 | `TheCocktailDB` | food | none | https://www.thecocktaildb.com/api.php | https://www.thecocktaildb.com/api/json/v1/1 | `https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita`<br/>`https://www.thecocktaildb.com/api/json/v1/1/random.php` |
| 28 | `SWAPI` | entertainment | none | https://swapi.py4e.com/documentation | https://swapi.py4e.com/api | `https://swapi.py4e.com/api/people/1/`<br/>`https://swapi.py4e.com/api/planets/1/` |
| 29 | `Rick and Morty API` | entertainment | none | https://rickandmortyapi.com/documentation | https://rickandmortyapi.com/api | `https://rickandmortyapi.com/api/character/1`<br/>`https://rickandmortyapi.com/api/episode/1` |
| 30 | `TVmaze` | media | none | https://www.tvmaze.com/api | https://api.tvmaze.com | `https://api.tvmaze.com/search/shows?q=girls`<br/>`https://api.tvmaze.com/shows/1` |
| 31 | `Jikan` | media | none (rate-limited) | https://docs.api.jikan.moe/ | https://api.jikan.moe/v4 | `https://api.jikan.moe/v4/anime/1`<br/>`https://api.jikan.moe/v4/top/anime?limit=5` |
| 32 | `Deezer API` | media | none for search | https://developers.deezer.com/api | https://api.deezer.com | `https://api.deezer.com/search?q=daft%20punk`<br/>`https://api.deezer.com/artist/27` |
| 33 | `iTunes Search API` | media | none | https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/index.html | https://itunes.apple.com | `https://itunes.apple.com/search?term=jack+johnson&limit=5`<br/>`https://itunes.apple.com/lookup?id=909253` |
| 34 | `LibriVox` | media | none | https://librivox.org/api/info | https://librivox.org/api/feed | `https://librivox.org/api/feed/audiobooks/?format=json&limit=5`<br/>`https://librivox.org/api/feed/audiobooks/?format=json&title=Sherlock` |
| 35 | `Art Institute of Chicago` | culture | none | https://api.artic.edu/docs/ | https://api.artic.edu/api/v1 | `https://api.artic.edu/api/v1/artworks?limit=5`<br/>`https://api.artic.edu/api/v1/artworks/129884` |
| 36 | `Met Museum Collection` | culture | none | https://metmuseum.github.io/ | https://collectionapi.metmuseum.org/public/collection/v1 | `https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds=11`<br/>`https://collectionapi.metmuseum.org/public/collection/v1/objects/436535` |
| 37 | `OpenAQ` | environment | none | https://docs.openaq.org/ | https://api.openaq.org/v2 | `https://api.openaq.org/v2/locations?limit=5`<br/>`https://api.openaq.org/v2/measurements?limit=5` |
| 38 | `CityBikes` | transport | none | https://api.citybik.es/v2/ | https://api.citybik.es/v2 | `https://api.citybik.es/v2/networks`<br/>`https://api.citybik.es/v2/networks/velo-antwerpen` |
| 39 | `BikeWise` | transport | none | https://www.bikewise.org/documentation/api_v2 | https://bikewise.org/api/v2 | `https://bikewise.org/api/v2/incidents?page=1&per_page=5`<br/>`https://bikewise.org/api/v2/locations?proximity=45.52,-122.67&proximity_square=10` |
| 40 | `Bored API` | entertainment | none | https://www.boredapi.com/documentation | https://www.boredapi.com/api | `https://www.boredapi.com/api/activity`<br/>`https://www.boredapi.com/api/activity?type=education` |
| 41 | `Genderize` | demographics | none (rate-limited) | https://genderize.io/ | https://api.genderize.io | `https://api.genderize.io/?name=peter`<br/>`https://api.genderize.io/?name[]=anna&name[]=john` |
| 42 | `Agify` | demographics | none (rate-limited) | https://agify.io/ | https://api.agify.io | `https://api.agify.io/?name=michael`<br/>`https://api.agify.io/?name[]=anna&name[]=john` |
| 43 | `Nationalize` | demographics | none (rate-limited) | https://nationalize.io/ | https://api.nationalize.io | `https://api.nationalize.io/?name=nathaniel`<br/>`https://api.nationalize.io/?name[]=luc&name[]=maria` |
| 44 | `Universities API` | education | none | https://github.com/Hipo/university-domains-list-api | https://universities.hipolabs.com | `https://universities.hipolabs.com/search?country=France`<br/>`https://universities.hipolabs.com/search?name=Paris` |
| 45 | `Data USA` | open-data | none | https://datausa.io/about/api/ | https://datausa.io/api | `https://datausa.io/api/?Geography=04000US06&measure=Population`<br/>`https://datausa.io/api/?drilldowns=Nation&measures=Population` |
| 46 | `World Bank` | open-data | none | https://datahelpdesk.worldbank.org/knowledgebase/topics/125589-developer-information | https://api.worldbank.org/v2 | `https://api.worldbank.org/v2/country/fr?format=json`<br/>`https://api.worldbank.org/v2/country/fr/indicator/SP.POP.TOTL?format=json` |
| 47 | `Open Trivia DB` | entertainment | none | https://opentdb.com/api_config.php | https://opentdb.com | `https://opentdb.com/api.php?amount=5`<br/>`https://opentdb.com/api_category.php` |
| 48 | `Numbers API` | education | none | http://numbersapi.com/ | http://numbersapi.com | `http://numbersapi.com/42/trivia?json`<br/>`http://numbersapi.com/random/math?json` |
| 49 | `Zippopotam` | geography | none | http://www.zippopotam.us/ | https://api.zippopotam.us | `https://api.zippopotam.us/us/90210`<br/>`https://api.zippopotam.us/fr/75001` |
| 50 | `Random User` | testing | none | https://randomuser.me/documentation | https://randomuser.me/api | `https://randomuser.me/api/?results=5`<br/>`https://randomuser.me/api/?nat=fr&results=5` |
