# Testimonials App

A React frontend with a FastAPI backend for collecting and displaying user testimonials.

## Project Structure

- `packages/api-backend/`: FastAPI backend service.
- `packages/web-app/`: React frontend application.

## API Backend (FastAPI)

Located in `packages/api-backend/main.py`.

### Endpoints
- `GET /` - Returns a welcome message.
- `GET /items/{item_id}` - Returns the item ID and an optional query parameter.
- `POST /api/v1/testimonials` - Submit a new testimonial.
- `GET /api/v1/testimonials` - List all testimonials.

## Web App (React)

Located in `packages/web-app/src/`.

### Key Components

#### `App.js`
The main application component that manages user input and passes it to the rendering components.

#### `ContentRenderer.js`
Renders testimonial content on the page.

#### `Testimonials.js`
Displays submitted testimonials from the backend.
