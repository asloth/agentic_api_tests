# API Documentation

## Base URL
```
https://api.example.com
```

## Authentication
All API requests require authentication using Bearer token in the header:
```
Authorization: Bearer YOUR_API_TOKEN
```

---

## Customers API

### Endpoints

#### Get All Customers
```http
GET /api/customer
```

**Response Example:**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane.smith@example.com"
  }
]
```

**Status Codes:**
- `200 OK` - Success
- `401 Unauthorized` - Invalid or missing token

---

#### Get Customer by ID
```http
GET /api/customer/{id}
```

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | Yes | Customer ID |

**Response Example:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com"
}
```

**Status Codes:**
- `200 OK` - Success
- `404 Not Found` - Customer not found
- `401 Unauthorized` - Invalid or missing token

---

#### Create Customer
```http
POST /api/customer
```

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com"
}
```

**Body Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Customer full name |
| email | string | Yes | Customer email address |

**Response Example:**
```json
{
  "id": 3,
  "name": "John Doe",
  "email": "john.doe@example.com"
}
```

**Status Codes:**
- `201 Created` - Customer successfully created
- `400 Bad Request` - Invalid input data
- `409 Conflict` - Email already exists
- `401 Unauthorized` - Invalid or missing token

---

#### Update Customer
```http
PUT /api/customer/{id}
```

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | Yes | Customer ID |

**Request Body:**
```json
{
  "name": "John Doe Updated",
  "email": "john.updated@example.com"
}
```

**Body Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | No | Customer full name |
| email | string | No | Customer email address |

**Response Example:**
```json
{
  "id": 1,
  "name": "John Doe Updated",
  "email": "john.updated@example.com"
}
```

**Status Codes:**
- `200 OK` - Customer successfully updated
- `404 Not Found` - Customer not found
- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Invalid or missing token

---

#### Delete Customer
```http
DELETE /api/customer/{id}
```

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | Yes | Customer ID |

**Response Example:**
```json
{
  "message": "Customer successfully deleted"
}
```

**Status Codes:**
- `200 OK` - Customer successfully deleted
- `404 Not Found` - Customer not found
- `401 Unauthorized` - Invalid or missing token

---

## Products API

### Endpoints

#### Get All Products
```http
GET /api/product
```

**Response Example:**
```json
[
  {
    "id": 1,
    "name": "Laptop"
  },
  {
    "id": 2,
    "name": "Mouse"
  }
]
```

**Status Codes:**
- `200 OK` - Success
- `401 Unauthorized` - Invalid or missing token

---

#### Get Product by ID
```http
GET /api/product/{id}
```

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | Yes | Product ID |

**Response Example:**
```json
{
  "id": 1,
  "name": "Laptop"
}
```

**Status Codes:**
- `200 OK` - Success
- `404 Not Found` - Product not found
- `401 Unauthorized` - Invalid or missing token

---

#### Create Product
```http
POST /api/product
```

**Request Body:**
```json
{
  "name": "Keyboard"
}
```

**Body Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Product name |

**Response Example:**
```json
{
  "id": 3,
  "name": "Keyboard"
}
```

**Status Codes:**
- `201 Created` - Product successfully created
- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Invalid or missing token

---

#### Update Product
```http
PUT /api/product/{id}
```

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | Yes | Product ID |

**Request Body:**
```json
{
  "name": "Mechanical Keyboard"
}
```

**Body Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Product name |

**Response Example:**
```json
{
  "id": 1,
  "name": "Mechanical Keyboard"
}
```

**Status Codes:**
- `200 OK` - Product successfully updated
- `404 Not Found` - Product not found
- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Invalid or missing token

---

#### Delete Product
```http
DELETE /api/product/{id}
```

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | Yes | Product ID |

**Response Example:**
```json
{
  "message": "Product successfully deleted"
}
```

**Status Codes:**
- `200 OK` - Product successfully deleted
- `404 Not Found` - Product not found
- `401 Unauthorized` - Invalid or missing token

---

## Database Schema

### Customers Table
```sql
CREATE TABLE customers (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Products Table
```sql
CREATE TABLE products (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

---

## Error Responses

All error responses follow this format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {}
  }
}
```

### Common Error Codes
- `INVALID_INPUT` - Request validation failed
- `NOT_FOUND` - Resource not found
- `UNAUTHORIZED` - Authentication required or failed
- `CONFLICT` - Resource already exists
- `INTERNAL_ERROR` - Server error

---

## Rate Limiting
- Rate limit: 100 requests per minute per API token
- Rate limit headers included in all responses:
  - `X-RateLimit-Limit`: Maximum requests allowed
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Time when limit resets (Unix timestamp)