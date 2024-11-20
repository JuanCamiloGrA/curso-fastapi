# FastAPI Subscriptions API

A robust REST API built with FastAPI for managing customer subscriptions, plans, and transactions. This project demonstrates modern Python web development practices and implements a real-world subscription management system.

## Project Overview

This API provides endpoints to manage:

- Customer accounts
- Subscription plans
- Customer subscriptions to plans
- Payment transactions
- Usage tracking
- Session management with SQLModel

## Technical Stack

- **FastAPI** - High-performance web framework
- **SQLModel** - SQL database ORM that combines SQLAlchemy and Pydantic
- **SQLite** - Lightweight database for development
- **Pytest** - Testing framework
- **Dependency Injection** - For database sessions and middleware
- **Type Annotations** - Leveraging Python's type system
- **Async/Await** - Asynchronous request handling

## Key Features

- RESTful API design principles
- Input validation with Pydantic models
- Database session management
- Request/Response logging middleware
- Error handling and HTTP status codes
- Pagination for list endpoints
- Automated testing setup

## Professional Skills Demonstrated

1. **API Design**

   - Clean routing structure
   - Consistent endpoint naming
   - Proper HTTP method usage
   - Status code implementation
   - Query parameter handling
2. **Database Design**

   - Relational data modeling
   - ORM implementation
   - Session management
   - Transaction handling
3. **Software Engineering Practices**

   - Dependency injection
   - Middleware implementation
   - Type safety
   - Modular code organization
   - Testing infrastructure
4. **Production Considerations**

   - Performance monitoring
   - Request logging
   - Error handling
   - Data validation
   - Scalable architecture

## Real-World Applications

This project mirrors enterprise subscription systems like:

- SaaS platforms
- Streaming services
- Membership systems
- Payment processing systems
- Customer management platforms

## Workplace Relevance

The skills demonstrated in this project are directly applicable to:

- Building scalable web services
- Implementing payment systems
- Managing customer data
- Creating subscription platforms
- Developing enterprise APIs

## Future Enhancements

- Authentication/Authorization
- Rate limiting
- Caching layer
- API documentation
- Database migrations
- Containerization
- CI/CD pipeline

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload

# Run tests
pytest
```

This project showcases professional-grade API development practices and provides a solid foundation for building production-ready subscription management systems.
