# API Documentation

## User Endpoints

### Get All Users

-   **URL:** `/users`
-   **Method:** `GET`
-   **Success Response:**
    ```json
    {
        "usernames": ["user1", "user2"]
    }
    ```

## Paper Endpoints

### Query Papers by Keywords

-   **URL:** `/query`
-   **Method:** `POST`
-   **Request Body:**
    ```json
    {
        "query": ["machine learning", "attention"],
        "start_time": 1672531200,
        "end_time": 1675209600,
        "start_index": 0,
        "end_index": 10
    }
    ```
-   **Success Response:**
    ```json
    {
        "articles": [
            {
                "arxiv_id": "2301.00001",
                "added_time": 1672531200,
                "submitted_time": 1672531100,
                "title": "Example Paper Title",
                "abstract": "This is an example abstract.",
                "authors": ["Author One", "Author Two"]
            }
        ]
    }
    ```

### Analyze Paper Section

-   **URL:** `/analysis`
-   **Method:** `POST`
-   **Request Body:**
    ```json
    {
        "arxiv_id": "2301.00001",
        "section": "abstract"
    }
    ```
-   **Success Response:**
    ```json
    {
        "analysis": "This is the analysis of the requested section."
    }
    ```

## User-Specific Endpoints

### Get User Keywords

-   **URL:** `/keywords`
-   **Method:** `GET`
-   **Query Parameters:**
    -   `username`: string
-   **Success Response:**
    ```json
    {
        "keywords": ["keyword1", "keyword2"]
    }
    ```

### Set User Keywords

-   **URL:** `/keywords`
-   **Method:** `POST`
-   **Request Body:**
    ```json
    {
        "username": "testuser",
        "keywords": ["new_keyword1", "new_keyword2"]
    }
    ```
-   **Success Response:**
    ```json
    {
        "success": true
    }
    ```

### Get User's Read Papers

-   **URL:** `/users/read_papers`
-   **Method:** `GET`
-   **Query Parameters:**
    -   `username`: string
-   **Success Response:**
    ```json
    {
        "arxiv_ids": ["2301.00001", "2301.00002"]
    }
    ```

### Set User's Read Papers

-   **URL:** `/users/read_papers`
-   **Method:** `POST`
-   **Request Body:**
    ```json
    {
        "username": "testuser",
        "arxiv_ids": ["2301.00001", "2301.00002", "2301.00003"]
    }
    ```
-   **Success Response:**
    ```json
    {
        "success": true
    }
    ```

### Get User's Favorite Papers

-   **URL:** `/users/favorite_papers`
-   **Method:** `GET`
-   **Query Parameters:**
    -   `username`: string
-   **Success Response:**
    ```json
    {
        "arxiv_ids": ["2301.00004"]
    }
    ```

### Set User's Favorite Papers

-   **URL:** `/users/favorite_papers`
-   **Method:** `POST`
-   **Request Body:**
    ```json
    {
        "username": "testuser",
        "arxiv_ids": ["2301.00004", "2301.00005"]
    }
    ```
-   **Success Response:**
    ```json
    {
        "success": true
    }
    ```