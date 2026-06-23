# HBnB Evolution - Architecture Reference

## Quick Reference Guide

### Package Diagram Components

#### Presentation Layer

- **API Endpoints:** REST API routes for all operations
- **Services:** Business logic wrappers for API handlers
- **Responsibility:** Handle HTTP requests/responses, input validation

#### Business Logic Layer  

- **User Model:** Handles user registration, profiles, validation
- **Place Model:** Manages property listings and metadata
- **Review Model:** Processes user reviews and ratings
- **Amenity Model:** Manages available amenities
- **Business Rules Engine:** Enforces all validation and business constraints

#### Persistence Layer

- **Database:** Physical data storage (specified in Part 3)
- **DAO/Repository Pattern:** Abstract data access operations

#### Facade Layer

- **Single entry point** for all business logic calls
- **Request routing** to appropriate models
- **Response packaging** for return to presentation layer
- **Decouples** layers from direct dependencies

---

## Class Relationships

### Ownership Hierarchy

```
User
├── owns → Place (1-to-many)
└── writes → Review (1-to-many)

Place
├── owned by → User (many-to-one)
├── has → Amenity (many-to-many)
└── receives → Review (1-to-many)

Review
├── written by → User (many-to-one)
└── about → Place (many-to-one)

Amenity
└── associated with → Place (many-to-many)
```

### Association Details

- **User → Place:** One user can own multiple places
- **User → Review:** One user can write multiple reviews (one per place)
- **Place → Review:** One place can receive multiple reviews
- **Place → Amenity:** One place can have multiple amenities; one amenity can be in multiple places

---

## API Endpoints Overview

### User Management

```
POST   /users               → Create new user
GET    /users/<id>          → Retrieve user details
PUT    /users/<id>          → Update user information
DELETE /users/<id>          → Delete user account
GET    /users/<id>/places   → List user's places
GET    /users/<id>/reviews  → List user's reviews
```

### Place Management

```
POST   /places              → Create new place
GET    /places              → List all places
GET    /places/<id>         → Get place details
PUT    /places/<id>         → Update place info
DELETE /places/<id>         → Delete place
POST   /places/<id>/amenities → Add amenity to place
DELETE /places/<id>/amenities/<amenity_id> → Remove amenity
```

### Review Management

```
POST   /reviews             → Submit new review
GET    /reviews             → List all reviews
GET    /reviews/<id>        → Get review details
PUT    /reviews/<id>        → Update review
DELETE /reviews/<id>        → Delete review
GET    /places/<id>/reviews → Get reviews for place
```

### Amenity Management

```
POST   /amenities           → Create new amenity
GET    /amenities           → List all amenities
GET    /amenities/<id>      → Get amenity details
PUT    /amenities/<id>      → Update amenity
DELETE /amenities/<id>      → Delete amenity
```

---

## Validation Rules by Entity

### User Validation

| Rule | Type | Requirement |
| ------ | ------ | ------------- |
| first_name | Required | Non-empty string, max 50 chars |
| last_name | Required | Non-empty string, max 50 chars |
| email | Required | Valid email format, unique |
| password | Required | Min 8 chars, 1 uppercase, 1 number |
| is_admin | Optional | Boolean, default false |

### Place Validation

| Rule | Type | Requirement |
| ------ | ------ | ------------- |
| title | Required | Non-empty string, max 128 chars |
| description | Optional | Max 2000 chars |
| price | Required | Positive number, max 2 decimals |
| latitude | Required | Float between -90 and 90 |
| longitude | Required | Float between -180 and 180 |
| owner | Required | Valid user ID |
| amenities | Optional | Array of valid amenity IDs |

### Review Validation

| Rule | Type | Requirement |
| ------ | ------ | ------------- |
| place_id | Required | Valid place ID |
| user_id | Required | Valid user ID |
| rating | Required | Integer 1-5 |
| comment | Optional | Max 500 chars |
| unique | Required | One review per user per place |

### Amenity Validation

| Rule | Type | Requirement |
|------|------|-------------|
| name | Required | Non-empty, unique, max 50 chars |
| description | Optional | Max 200 chars |

---

## Data Model - SQL Schema Preview

### Users Table

```
CREATE TABLE users (
    id UUID PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

### Places Table

```
CREATE TABLE places (
    id UUID PRIMARY KEY,
    title VARCHAR(128) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Reviews Table

```
CREATE TABLE reviews (
    id UUID PRIMARY KEY,
    place_id UUID NOT NULL,
    user_id UUID NOT NULL,
    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    UNIQUE(place_id, user_id),
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Amenities Table

```
CREATE TABLE amenities (
    id UUID PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(200),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

### Place_Amenities Junction Table

```
CREATE TABLE place_amenities (
    place_id UUID NOT NULL,
    amenity_id UUID NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);
```

---

## Facade Pattern Benefits

1. **Simplification:** Complex interactions hidden behind simple interface
2. **Decoupling:** Presentation layer doesn't need to know about business logic implementation
3. **Centralization:** All business logic routing in one place
4. **Maintainability:** Changes to models don't affect API layer
5. **Security:** Single validation point for all requests
6. **Consistency:** Uniform error handling and response format

---

## Design Pattern Summary

### Patterns Used

1. **Layered Architecture:** Separation of concerns across three layers
2. **Facade Pattern:** Unified interface for complex subsystems
3. **Repository Pattern:** Data access abstraction (Persistence Layer)
4. **Model-View-Presenter:** API → Model → Database flow
5. **Entity Pattern:** Domain-driven design for core entities

### Why These Patterns?

- **Scalability:** Easy to add new features without modifying existing code
- **Testability:** Each layer can be tested independently
- **Maintainability:** Clear responsibilities and clean interfaces
- **Flexibility:** Database can be changed without affecting business logic
- **Reusability:** Business logic can be used by multiple API versions

---

## Implementation Checklist

### Phase 1: Models

- [ ] Implement User model with validation
- [ ] Implement Place model with validation
- [ ] Implement Review model with validation
- [ ] Implement Amenity model with validation
- [ ] Create base Entity class for common attributes

### Phase 2: Business Logic

- [ ] Implement Facade class
- [ ] Add user registration logic
- [ ] Add place creation logic
- [ ] Add review submission logic
- [ ] Add amenity management logic

### Phase 3: Persistence

- [ ] Design database schema
- [ ] Create repository classes
- [ ] Implement data access methods
- [ ] Add database validation

### Phase 4: API

- [ ] Create API endpoints for users
- [ ] Create API endpoints for places
- [ ] Create API endpoints for reviews
- [ ] Create API endpoints for amenities

### Phase 5: Testing

- [ ] Unit tests for models
- [ ] Integration tests for Facade
- [ ] End-to-end tests for API endpoints
- [ ] Performance testing

---

## Common Scenarios and Flows

### Scenario 1: New User Registration

1. User submits registration form
2. API validates input format
3. Facade checks email uniqueness
4. User model hashes password
5. Database stores new user
6. API returns user ID and confirmation

### Scenario 2: User Lists a Property

1. Owner navigates to "List Property"
2. Fills in place details
3. API validates coordinates
4. Facade verifies owner exists
5. Place model calculates/stores data
6. Database stores place
7. User receives confirmation with place ID

### Scenario 3: User Reviews a Place

1. User submits review form
2. API validates rating (1-5)
3. Facade checks review doesn't already exist
4. Verifies both place and user exist
5. Review model stores review
6. Database stores review
7. UI updates with new review

### Scenario 4: Browsing Places

1. User requests places list
2. API adds pagination parameters
3. Facade retrieves places from database
4. For each place, fetch amenities
5. Calculate average rating from reviews
6. Format and return to API
7. UI displays places with amenities and ratings

---

## Performance Considerations

1. **Caching:** Store frequently accessed amenities
2. **Indexing:** Index user emails, place coordinates
3. **Pagination:** Limit places list to 10-20 per request
4. **Lazy Loading:** Load place amenities only when needed
5. **Connection Pooling:** Reuse database connections

---

## Security Considerations

1. **Password:** Hash with bcrypt or similar
2. **Authentication:** Implement JWT or session tokens
3. **Authorization:** Check user permissions before operations
4. **Input Validation:** Sanitize all user inputs
5. **SQL Injection:** Use parameterized queries
6. **Rate Limiting:** Limit API requests per user
7. **HTTPS:** Always use encrypted connections

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-06-03 | Initial architecture documentation |
