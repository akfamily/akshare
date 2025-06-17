```mermaid

graph LR

    Core_Infrastructure_Utilities["Core Infrastructure & Utilities"]

    Exception_Handling["Exception Handling"]

    Global_Configuration_Proxy_Management["Global Configuration & Proxy Management"]

    HTTP_Request_Handler["HTTP Request Handler"]

    General_Utilities["General Utilities"]

    Progress_Bar_Utility["Progress Bar Utility"]

    API_Token_Management["API Token Management"]

    Common_Constants["Common Constants"]

    Robust_JSON_Decoder["Robust JSON Decoder"]

    HTTP_Request_Handler -- "depends on" --> Exception_Handling

    HTTP_Request_Handler -- "depends on" --> Global_Configuration_Proxy_Management

    General_Utilities -- "depends on" --> Progress_Bar_Utility

    API_Token_Management -- "depends on" --> Common_Constants

    Core_Infrastructure_Utilities -- "provides services to" --> StockMarketDataSource

    Core_Infrastructure_Utilities -- "provides services to" --> DataVisualization

    Exception_Handling -- "is part of" --> Core_Infrastructure_Utilities

    Global_Configuration_Proxy_Management -- "is part of" --> Core_Infrastructure_Utilities

    HTTP_Request_Handler -- "is part of" --> Core_Infrastructure_Utilities

    General_Utilities -- "is part of" --> Core_Infrastructure_Utilities

    Progress_Bar_Utility -- "is part of" --> Core_Infrastructure_Utilities

    API_Token_Management -- "is part of" --> Core_Infrastructure_Utilities

    Common_Constants -- "is part of" --> Core_Infrastructure_Utilities

    Robust_JSON_Decoder -- "is part of" --> Core_Infrastructure_Utilities

    click Core_Infrastructure_Utilities href "https://github.com/akfamily/akshare/blob/main/.codeboarding//Core_Infrastructure_Utilities.md" "Details"

```

[![CodeBoarding](https://img.shields.io/badge/Generated%20by-CodeBoarding-9cf?style=flat-square)](https://github.com/CodeBoarding/GeneratedOnBoardings)[![Demo](https://img.shields.io/badge/Try%20our-Demo-blue?style=flat-square)](https://www.codeboarding.org/demo)[![Contact](https://img.shields.io/badge/Contact%20us%20-%20contact@codeboarding.org-lightgrey?style=flat-square)](mailto:contact@codeboarding.org)



## Component Details



This is the foundational layer of `akshare`, providing essential, widely-used helper functions and global configurations. It encompasses robust JSON decoding, progress bar display, general function utilities, and critical proxy and API token management. Crucially, it centralizes all HTTP requests to external data sources, including retry mechanisms and basic error handling, and defines a comprehensive set of custom exception classes to standardize error reporting across the library.



### Core Infrastructure & Utilities

This is the foundational layer of `akshare`, providing essential, widely-used helper functions and global configurations. It encompasses robust JSON decoding, progress bar display, general function utilities, and critical proxy and API token management. Crucially, it centralizes all HTTP requests to external data sources, including retry mechanisms and basic error handling, and defines a comprehensive set of custom exception classes to standardize error reporting across the library.





**Related Classes/Methods**: _None_



### Exception Handling

Defines a comprehensive set of custom exception classes (`AkshareException`, `APIError`, `NetworkError`, `RateLimitError`, `DataParsingError`, `InvalidParameterError`) to standardize error reporting across the `akshare` library. This ensures consistent and clear error messages for developers and users.





**Related Classes/Methods**:



- `Exception Handling` (1:1)





### Global Configuration & Proxy Management

Manages global settings, primarily proxy configurations, using a singleton pattern (`AkshareConfig`). It provides methods to set and retrieve proxies globally and includes a `ProxyContext` for temporary proxy adjustments, crucial for network flexibility.





**Related Classes/Methods**:



- `Global Configuration & Proxy Management` (1:1)





### HTTP Request Handler

Centralizes all HTTP GET requests to external data sources. It implements robust retry mechanisms with exponential backoff and comprehensive error handling, raising specific custom exceptions defined in `akshare.exceptions`. It also integrates with `Global Configuration & Proxy Management` for proxy usage.





**Related Classes/Methods**:



- `HTTP Request Handler` (1:1)





### General Utilities

Provides a collection of widely-used helper functions for common data-related tasks, such as fetching paginated data from external sources and standardizing Pandas DataFrame columns. It integrates with the `Progress Bar Utility` for user feedback.





**Related Classes/Methods**:



- `General Utilities` (1:1)





### Progress Bar Utility

Offers a flexible way to display progress bars (`tqdm`) in different Python environments (e.g., console, Jupyter Notebook). This enhances user experience by providing visual feedback during long-running data fetching or processing operations.





**Related Classes/Methods**:



- `Progress Bar Utility` (1:1)





### API Token Management

Handles the secure storage and retrieval of API tokens. It manages the persistence of these tokens, typically in a user-specific file, ensuring authenticated access to various data providers.





**Related Classes/Methods**:



- `API Token Management` (1:1)





### Common Constants

Stores global constants and default values, such as standard HTTP headers and file paths for token storage. This centralizes frequently used values, promoting consistency and ease of modification across the library.





**Related Classes/Methods**:



- `Common Constants` (1:1)





### Robust JSON Decoder

Provides an advanced JSON decoding mechanism, likely for handling non-standard or complex JSON structures that might be encountered from diverse financial data sources, ensuring reliable data parsing.





**Related Classes/Methods**:



- `Robust JSON Decoder` (1:1)









### [FAQ](https://github.com/CodeBoarding/GeneratedOnBoardings/tree/main?tab=readme-ov-file#faq)