# HBnB Evolution - Business Rules & Requirements

## Business Rules Engine

### User-Related Rules

#### Registration Rules

1. **Email Uniqueness**
   - Email must be unique across the system
   - No two users can share the same email
   - Emails should be case-insensitive for comparison

2. **Password Requirements**
   - Minimum 8 characters
   - Must contain at least one uppercase letter
   - Must contain at least one number
   - Must not be the same as username or email

3. **Name Validation**
   - First name and last name are required
   - Names must be 1-50 characters
   - Special characters allowed (hyphens, apostrophes)

4. **Account Type**
   - Default account type is regular user
   - Admin status is set during initial registration or by existing admin
   - Only admins can modify other users' admin status

#### User Profile Management Rules

1. **Update Restrictions**
   - Users can only modify their own profile
   - Admins can modify any user profile
   - Email changes require verification

2. **Deletion Rules**
   - Users can delete their own account
   - Admins can delete any account
   - User deletion cascades: deletes all owned places and written reviews

#### User Authentication Rules

1. **Login Validation**
   - Email and password must be correct
   - Passwords are case-sensitive
   - Failed attempts may be tracked (for Part 4)

---

### Place-Related Rules

#### Place Creation Rules

1. **Ownership**
   - Only registered users can create places
   - Owner must exist in the system
   - Each place has exactly one owner

2. **Coordinate Validation**
   - Latitude must be between -90 and 90
   - Longitude must be between -180 and 180
   - Both values should be valid floating-point numbers

3. **Price Validation**
   - Price must be positive (> 0)
   - Price maximum reasonable limit: $10,000
   - Price stored with 2 decimal places

4. **Title and Description**
   - Title is required (1-128 characters)
   - Description is optional (max 2000 characters)
   - No excessive whitespace allowed

#### Place Modification Rules

1. **Edit Restrictions**
   - Only place owner can modify place details
   - Admins can modify any place
   - Place owner can be transferred (admin action)

2. **Deletion Rules**
   - Place deletion cascades to all associated reviews
   - Place owner can delete their own place
   - Admins can delete any place

3. **Amenity Management**
   - Owner can add/remove amenities from their place
   - Amenities must exist before association
   - Place can have 0 or more amenities

---

### Review-Related Rules

#### Review Submission Rules

1. **Eligibility**
   - Only registered users can submit reviews
   - User must be different from place owner
   - User should have had a booking (implementation detail for Part 4)

2. **Rating Requirements**
   - Rating is required
   - Rating must be an integer between 1 and 5
   - 1 = Poor, 5 = Excellent

3. **Comment Guidelines**
   - Comment is optional
   - Maximum 500 characters if provided
   - Profanity filtering (optional, Part 4)

4. **Uniqueness Constraint**
   - One review per user per place maximum
   - User cannot submit multiple reviews for the same place
   - User can review different places

#### Review Modification Rules

1. **Edit Restrictions**
   - Only review author can edit their review
   - Admins can edit any review
   - Rating and comment can be updated
   - Updated timestamp should reflect modification

2. **Deletion Rules**
   - Review author can delete their review
   - Admins can delete any review
   - Deleted reviews don't affect place's average rating
   - Review deletion doesn't affect place listing

---

### Amenity-Related Rules

#### Amenity Management Rules

1. **Creation**
   - Amenity name must be unique
   - Name is required (1-50 characters)
   - Description is optional (max 200 characters)
   - Only admins can create amenities

2. **Modification**
   - Name cannot be changed (use delete and create)
   - Description can be updated
   - Only admins can modify amenities

3. **Deletion**
   - Amenities can be deleted by admins
   - Deleting amenity removes association from all places
   - Places remain unchanged, only amenity association removed

4. **Availability**
   - Amenities are platform-wide (not per-place)
   - All users can see available amenities
   - Multiple places can share same amenities

---

## Data Integrity Rules

### Referential Integrity

1. **Foreign Key Constraints**
   - Place.owner_id must reference valid User.id
   - Review.user_id must reference valid User.id
   - Review.place_id must reference valid Place.id
   - PlaceAmenity.place_id must reference valid Place.id
   - PlaceAmenity.amenity_id must reference valid Amenity.id

2. **Cascade Rules**
   - Delete User → Delete all User's Places → Delete all Place's Reviews
   - Delete User → Delete all User's Reviews
   - Delete Place → Delete all Place's Reviews
   - Delete Amenity → Remove association with Places (keep places)

### Data Consistency

1. **Timestamps**
   - created_at is immutable (set once)
   - updated_at changes with each modification
   - Both must be in ISO 8601 format
   - Server time is authority (not client time)

2. **UUID Generation**
   - All IDs should be UUID v4
   - IDs are immutable
   - IDs should be globally unique

---

## Validation Rules Summary Table

### Field-Level Validation

| Entity | Field | Type | Constraints | Rules |
| -------- | ------- | ------ | ------------- | ------- |
| User | id | UUID | Required, Unique | Auto-generated |
| User | first_name | String | Required | 1-50 chars, alphanumeric + spaces |
| User | last_name | String | Required | 1-50 chars, alphanumeric + spaces |
| User | email | String | Required, Unique | Valid email format |
| User | password | String | Required | Min 8 chars, 1 upper, 1 number |
| User | is_admin | Boolean | Optional | Default: false |
| User | created_at | DateTime | Required | Auto-set, immutable |
| User | updated_at | DateTime | Required | Auto-set, updates on modify |
| Place | id | UUID | Required, Unique | Auto-generated |
| Place | title | String | Required | 1-128 chars, non-empty |
| Place | description | String | Optional | Max 2000 chars |
| Place | price | Decimal | Required | > 0, max 999999.99 |
| Place | latitude | Float | Required | -90 to 90 |
| Place | longitude | Float | Required | -180 to 180 |
| Place | owner_id | UUID | Required | Must exist in users |
| Place | created_at | DateTime | Required | Auto-set, immutable |
| Place | updated_at | DateTime | Required | Auto-set, updates on modify |
| Review | id | UUID | Required, Unique | Auto-generated |
| Review | place_id | UUID | Required | Must exist in places |
| Review | user_id | UUID | Required | Must exist in users |
| Review | rating | Integer | Required | 1 to 5 inclusive |
| Review | comment | String | Optional | Max 500 chars |
| Review | created_at | DateTime | Required | Auto-set, immutable |
| Review | updated_at | DateTime | Required | Auto-set, updates on modify |
| Amenity | id | UUID | Required, Unique | Auto-generated |
| Amenity | name | String | Required, Unique | 1-50 chars, non-empty |
| Amenity | description | String | Optional | Max 200 chars |
| Amenity | created_at | DateTime | Required | Auto-set, immutable |
| Amenity | updated_at | DateTime | Required | Auto-set, updates on modify |

---

## Business Logic Workflows

### Workflow 1: User Registration and Profile Setup

```
1. User provides: first_name, last_name, email, password
2. Validate all fields against constraints
3. Check email doesn't already exist
4. Hash password
5. Create user with is_admin=false
6. Set created_at and updated_at
7. Return user_id to client
8. Send confirmation email (Part 4)
```

### Workflow 2: User Creates a Place Listing

```
1. User (must be logged in) provides: title, description, price, latitude, longitude
2. Verify user exists and is not deleted
3. Validate all place fields
4. Create place with owner_id set to current user
5. Set created_at and updated_at
6. Return place_id and confirmation
```

### Workflow 3: User Adds Amenity to Place

```
1. User provides: place_id, amenity_id
2. Verify place exists and user is owner (or is admin)
3. Verify amenity exists
4. Check amenity not already associated with place
5. Create association in PlaceAmenities table
6. Return success
```

### Workflow 4: User Submits a Review

```
1. User provides: place_id, rating, comment
2. Verify user is not place owner
3. Verify place exists
4. Validate rating is 1-5
5. Check user hasn't already reviewed this place
6. Create review with user_id and place_id
7. Set created_at and updated_at
8. Return review_id
```

### Workflow 5: Admin Modifies a User

```
1. Admin provides: user_id, field_name, new_value
2. Verify requesting user is admin
3. Verify target user exists
4. Validate new value against constraints
5. Update field with new value
6. Update updated_at timestamp
7. Return success
```

---

## Error Handling Rules

### HTTP Status Codes

| Status | Scenario | Message |
| -------- | ---------- | --------- |
| 200 | Success (GET, PUT) | OK |
| 201 | Success (POST) | Created |
| 204 | Success (DELETE) | No Content |
| 400 | Invalid input | Bad Request - field validation error |
| 401 | Not authenticated | Unauthorized - no token/session |
| 403 | Not authorized | Forbidden - insufficient permissions |
| 404 | Resource not found | Not Found - ID doesn't exist |
| 409 | Conflict | Conflict - duplicate email/unique constraint |
| 422 | Invalid data | Unprocessable Entity - business logic violation |
| 500 | Server error | Internal Server Error |

### Specific Error Scenarios

#### User Operations

- **Invalid email format:** 400 Bad Request
- **Email already exists:** 409 Conflict
- **Weak password:** 422 Unprocessable Entity
- **User not found:** 404 Not Found
- **Unauthorized modification:** 403 Forbidden

#### Place Operations

- **Invalid coordinates:** 400 Bad Request
- **Price not positive:** 422 Unprocessable Entity
- **User doesn't exist:** 404 Not Found
- **Not place owner:** 403 Forbidden
- **Place not found:** 404 Not Found

#### Review Operations

- **Rating out of range:** 400 Bad Request
- **Place not found:** 404 Not Found
- **User is place owner:** 422 Unprocessable Entity
- **Review already exists for user/place:** 409 Conflict
- **Review not found:** 404 Not Found

#### Amenity Operations

- **Amenity name exists:** 409 Conflict
- **Amenity not found:** 404 Not Found
- **Not authorized (not admin):** 403 Forbidden

---

## Performance and Optimization Rules

### Indexing Strategy

```sql
-- Users table
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_is_admin ON users(is_admin);

-- Places table
CREATE INDEX idx_places_owner_id ON places(owner_id);
CREATE INDEX idx_places_coordinates ON places(latitude, longitude);
CREATE INDEX idx_places_price ON places(price);

-- Reviews table
CREATE INDEX idx_reviews_place_id ON reviews(place_id);
CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_reviews_place_user ON reviews(place_id, user_id);

-- PlaceAmenities table
CREATE INDEX idx_place_amenities_place_id ON place_amenities(place_id);
CREATE INDEX idx_place_amenities_amenity_id ON place_amenities(amenity_id);

-- Amenities table
CREATE INDEX idx_amenities_name ON amenities(name);
```

### Query Optimization Rules

1. Always limit result sets (use pagination)
2. Use indexes for WHERE clauses
3. Eager load amenities with places to avoid N+1 queries
4. Cache frequently accessed amenities list
5. Use database connection pooling

### Caching Rules

1. Cache amenities list (invalidate on amenities update)
2. Cache place details for 5 minutes
3. Cache average ratings for places
4. Cache user count statistics for admins
5. Invalidate cache on any write operation

---

## Security Rules

### Authentication & Authorization

1. All write operations require authentication
2. Users can only read/write their own data
3. Admins can read/write any data
4. Password must be hashed before storage (never stored plain text)
5. Password reset requires email verification

### Input Validation

1. All inputs must be validated on both client and server
2. String lengths must be enforced
3. Numeric ranges must be enforced
4. Email format must be valid
5. No SQL injection allowed (use parameterized queries)

### Data Protection

1. Sensitive fields (password) should never be returned in API responses
2. User email should be obfuscated for non-admins
3. All data transfers should use HTTPS
4. Rate limiting on all endpoints
5. CORS configuration to prevent cross-site requests

---

## Audit and Logging Rules

### Audit Trail

1. Track all user logins (Part 4)
2. Log all admin actions
3. Log all data modifications with before/after values
4. Include timestamp and user ID in all logs
5. Retain logs for 6 months minimum

### Sensitive Operations

- User password change
- User account deletion
- Admin status change
- Large data modifications
- Failed login attempts (Part 4)

---

## Business Rules Priority Matrix

| Rule | Priority | Enforced By | Impact |
| ------ | ---------- | ------------ | -------- |
| Email uniqueness | Critical | Database + Application | Data integrity |
| Password requirements | Critical | Application | Security |
| One review per user per place | Critical | Database | Data integrity |
| Coordinate validation | High | Application | Data quality |
| Price must be positive | High | Application | Data quality |
| Rating must be 1-5 | High | Application | Data quality |
| User ownership of places | High | Application | Authorization |
| Owner can't review own place | Medium | Application | Business logic |
| Timestamps auto-generated | Medium | Application | Audit trail |
| Amenity cascading | Low | Database | Cleanup |

---

## Document Version

- **Version:** 1.0
- **Last Updated:** 2026-06-03
- **Status:** Complete - Ready for Implementation
