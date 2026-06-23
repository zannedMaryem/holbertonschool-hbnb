# HBnB Evolution - Mermaid Diagrams Reference

This file contains all Mermaid diagram syntax used in the technical documentation. These diagrams can be viewed in any Mermaid-compatible tool or imported into draw.io.

## Package Diagram

```mermaid
graph TB
    subgraph Presentation["Presentation Layer"]
        API["API Endpoints"]
        Services["Services"]
    end
    
    subgraph Facade["Facade Layer"]
        FacadeInterface["Facade Interface<br/>(Unified Access Point)"]
    end
    
    subgraph BusinessLogic["Business Logic Layer"]
        UserModel["User Model"]
        PlaceModel["Place Model"]
        ReviewModel["Review Model"]
        AmenityModel["Amenity Model"]
        BusinessRules["Business Rules Engine"]
    end
    
    subgraph Persistence["Persistence Layer"]
        Database["Database<br/>(Storage)"]
    end
    
    API -->|requests| FacadeInterface
    Services -->|requests| FacadeInterface
    FacadeInterface -->|delegates| UserModel
    FacadeInterface -->|delegates| PlaceModel
    FacadeInterface -->|delegates| ReviewModel
    FacadeInterface -->|delegates| AmenityModel
    FacadeInterface -->|routes business logic| BusinessRules
    UserModel -->|CRUD operations| Database
    PlaceModel -->|CRUD operations| Database
    ReviewModel -->|CRUD operations| Database
    AmenityModel -->|CRUD operations| Database
    BusinessRules -->|validates & enforces| UserModel
    BusinessRules -->|validates & enforces| PlaceModel
    BusinessRules -->|validates & enforces| ReviewModel
    BusinessRules -->|validates & enforces| AmenityModel
    
    style Presentation fill:#e1f5ff
    style Facade fill:#fff9c4
    style BusinessLogic fill:#f3e5f5
    style Persistence fill:#e8f5e9
```

## Class Diagram

```mermaid
classDiagram
    class BaseEntity {
        -id: UUID
        -created_at: DateTime
        -updated_at: DateTime
        +get_id()
        +to_dict()
        +update()
    }
    
    class User {
        -first_name: String
        -last_name: String
        -email: String
        -password: String
        -is_admin: Boolean
        +register(): Boolean
        +update_profile(data): Boolean
        +validate_email(): Boolean
        +get_places()
        +get_reviews()
        +delete()
    }
    
    class Place {
        -title: String
        -description: String
        -price: Float
        -latitude: Float
        -longitude: Float
        -owner: User
        -amenities: List~Amenity~
        +create(): Boolean
        +update(data): Boolean
        +add_amenity(amenity): Boolean
        +remove_amenity(amenity): Boolean
        +get_amenities()
        +get_reviews()
        +delete()
    }
    
    class Review {
        -place: Place
        -user: User
        -rating: Integer
        -comment: String
        +create(): Boolean
        +update(data): Boolean
        +validate_rating(): Boolean
        +delete()
    }
    
    class Amenity {
        -name: String
        -description: String
        +create(): Boolean
        +update(data): Boolean
        +delete()
    }
    
    class PlaceAmenityAssociation {
        -place: Place
        -amenity: Amenity
    }
    
    BaseEntity <|-- User
    BaseEntity <|-- Place
    BaseEntity <|-- Review
    BaseEntity <|-- Amenity
    
    Place "1" --> "*" Amenity: has
    Place "1" --> "*" Review: receives
    User "1" --> "*" Place: owns
    User "1" --> "*" Review: writes
    Review "1" --> "1" Place: reviews
    Review "1" --> "1" User: from
```

## Sequence Diagram 1: User Registration

```mermaid
sequenceDiagram
    participant Client
    participant API as API Endpoint
    participant Facade
    participant UserModel as User Model
    participant Validation as Validation Rules
    participant Database as Persistence Layer
    
    Client->>API: POST /users<br/>{first_name, last_name, email, password}
    activate API
    
    API->>Facade: register_user(user_data)
    activate Facade
    
    Facade->>UserModel: create_user(user_data)
    activate UserModel
    
    UserModel->>Validation: validate_email(email)
    activate Validation
    Validation-->>UserModel: is_valid
    deactivate Validation
    
    UserModel->>Validation: validate_password(password)
    activate Validation
    Validation-->>UserModel: is_strong
    deactivate Validation
    
    UserModel->>Validation: check_email_unique(email)
    activate Validation
    Validation->>Database: query_user_by_email(email)
    Database-->>Validation: null
    Validation-->>UserModel: email_available
    deactivate Validation
    
    UserModel->>Database: save_user(user_data)
    activate Database
    Database-->>UserModel: user_id, created_at
    deactivate Database
    
    UserModel-->>Facade: user_created
    deactivate UserModel
    
    Facade-->>API: success_response
    deactivate Facade
    
    API-->>Client: 201 Created<br/>{user_id, email, created_at}
    deactivate API
```

## Sequence Diagram 2: Place Creation

```mermaid
sequenceDiagram
    participant Client
    participant API as API Endpoint
    participant Facade
    participant PlaceModel as Place Model
    participant Validation as Business Rules
    participant UserModel as User Model
    participant Database as Persistence Layer
    
    Client->>API: POST /places<br/>{title, description, price, latitude, longitude, owner_id}
    activate API
    
    API->>Facade: create_place(place_data, owner_id)
    activate Facade
    
    Facade->>UserModel: verify_user_exists(owner_id)
    activate UserModel
    UserModel->>Database: get_user(owner_id)
    Database-->>UserModel: user_object
    UserModel-->>Facade: user_verified
    deactivate UserModel
    
    Facade->>PlaceModel: create_place(place_data)
    activate PlaceModel
    
    PlaceModel->>Validation: validate_price(price)
    activate Validation
    Validation-->>PlaceModel: price_valid
    deactivate Validation
    
    PlaceModel->>Validation: validate_coordinates(latitude, longitude)
    activate Validation
    Validation-->>PlaceModel: coordinates_valid
    deactivate Validation
    
    PlaceModel->>Database: save_place(place_data)
    activate Database
    Database-->>PlaceModel: place_id, created_at
    deactivate Database
    
    PlaceModel-->>Facade: place_created
    deactivate PlaceModel
    
    Facade-->>API: success_response
    deactivate Facade
    
    API-->>Client: 201 Created<br/>{place_id, owner_id, created_at}
    deactivate API
```

## Sequence Diagram 3: Review Submission

```mermaid
sequenceDiagram
    participant Client
    participant API as API Endpoint
    participant Facade
    participant ReviewModel as Review Model
    participant Validation as Business Rules
    participant UserModel as User Model
    participant PlaceModel as Place Model
    participant Database as Persistence Layer
    
    Client->>API: POST /reviews<br/>{place_id, user_id, rating, comment}
    activate API
    
    API->>Facade: submit_review(review_data)
    activate Facade
    
    Facade->>PlaceModel: verify_place_exists(place_id)
    activate PlaceModel
    PlaceModel->>Database: get_place(place_id)
    Database-->>PlaceModel: place_object
    PlaceModel-->>Facade: place_verified
    deactivate PlaceModel
    
    Facade->>UserModel: verify_user_exists(user_id)
    activate UserModel
    UserModel->>Database: get_user(user_id)
    Database-->>UserModel: user_object
    UserModel-->>Facade: user_verified
    deactivate UserModel
    
    Facade->>ReviewModel: create_review(review_data)
    activate ReviewModel
    
    ReviewModel->>Validation: validate_rating(rating)
    activate Validation
    Validation-->>ReviewModel: rating_valid_1_to_5
    deactivate Validation
    
    ReviewModel->>Validation: check_duplicate_review(user_id, place_id)
    activate Validation
    Validation->>Database: query_existing_review(user_id, place_id)
    Database-->>Validation: null
    Validation-->>ReviewModel: no_duplicate
    deactivate Validation
    
    ReviewModel->>Database: save_review(review_data)
    activate Database
    Database-->>ReviewModel: review_id, created_at
    deactivate Database
    
    ReviewModel-->>Facade: review_created
    deactivate ReviewModel
    
    Facade-->>API: success_response
    deactivate Facade
    
    API-->>Client: 201 Created<br/>{review_id, rating, created_at}
    deactivate API
```

## Sequence Diagram 4: Fetching Places List

```mermaid
sequenceDiagram
    participant Client
    participant API as API Endpoint
    participant Facade
    participant PlaceModel as Place Model
    participant Database as Persistence Layer
    participant AmenityModel as Amenity Model
    
    Client->>API: GET /places?limit=10&offset=0
    activate API
    
    API->>Facade: get_places_list(limit, offset)
    activate Facade
    
    Facade->>PlaceModel: fetch_all_places(limit, offset)
    activate PlaceModel
    
    PlaceModel->>Database: query_places(limit, offset)
    activate Database
    Database-->>PlaceModel: places_data_list
    deactivate Database
    
    loop For each place
        PlaceModel->>AmenityModel: get_place_amenities(place_id)
        activate AmenityModel
        AmenityModel->>Database: query_amenities_by_place(place_id)
        Database-->>AmenityModel: amenities_list
        AmenityModel-->>PlaceModel: amenities_data
        deactivate AmenityModel
        
        PlaceModel->>Database: get_reviews_count(place_id)
        Database-->>PlaceModel: review_count
    end
    
    PlaceModel-->>Facade: formatted_places_list
    deactivate PlaceModel
    
    Facade-->>API: response_data
    deactivate Facade
    
    API-->>Client: 200 OK<br/>[{place_id, title, price, amenities, reviews_count}, ...]
    deactivate API
```

## Entity Relationship Diagram

```mermaid
graph LR
    User[User<br/>first_name<br/>last_name<br/>email<br/>is_admin]
    Place[Place<br/>title<br/>description<br/>price<br/>latitude<br/>longitude]
    Review[Review<br/>rating<br/>comment]
    Amenity[Amenity<br/>name<br/>description]
    
    User -->|owns 1..n| Place
    User -->|writes 1..n| Review
    Review -->|about 1| Place
    Place -->|receives 1..n| Review
    Place -->|has 0..n| Amenity
    Amenity -->|on 0..n| Place
    
    style User fill:#c8e6c9
    style Place fill:#bbdefb
    style Review fill:#ffe0b2
    style Amenity fill:#f8bbd0
```

## State Diagram - User Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Registration
    Registration --> NewUser: Account Created
    NewUser --> Active: Email Verified
    Active --> Inactive: User Deleted
    Inactive --> [*]
    Active --> Suspended: Admin Action
    Suspended --> Active: Admin Reinstate
    Suspended --> Inactive: Admin Delete
    
    note right of Registration
        Email validation
        Password hashing
        Account creation
    end note
    
    note right of Active
        User can list places
        User can write reviews
        User can manage profile
    end note
```

## Import Instructions

### For draw.io

1. Open draw.io
2. Click "File" → "Import from" → "URL"
3. Paste the Mermaid code wrapped in mermaid tags
4. Or use the Mermaid plugin if available

### For GitHub

Mermaid diagrams render directly in markdown:

- Copy the diagram code (without backticks)
- Paste in .md file
- GitHub will render automatically

### For Confluence/Jira

1. Install Mermaid plugin
2. Use syntax:

   ```
   {{mermaid
   <diagram-code>
   }}
   ```

### For VS Code

Install the Mermaid extension and view diagrams directly.

---

## Diagram Descriptions

| Diagram | Purpose | Use Case |
| --------- | --------- | ---------- |
| Package | Show system architecture | Understanding layer organization |
| Class | Show entity relationships | Implementation guide |
| Sequence 1 | User registration flow | Test user creation |
| Sequence 2 | Place creation flow | Test property listing |
| Sequence 3 | Review submission | Test review system |
| Sequence 4 | Data retrieval | Test list endpoints |
| Entity Relationship | Show data model | Database design |
| State | Show entity lifecycle | Understand entity states |

---

**Version:** 1.0  
**Last Updated:** 2026-06-03
