from enum import Enum


class NotificationEventType(str, Enum):
    WEBSITE_DOWN = "website_down"
    WEBSITE_RECOVERED = "website_recovered"
    WEBSITE_DEGRADED = "website_degraded"
    WEBSITE_RESTORED = "website_restored"

    WORDPRESS_DATABASE_ERROR = "wordpress_database_error"
    WORDPRESS_MAINTENANCE = "wordpress_maintenance"
    WORDPRESS_REST_API_DOWN = "wordpress_rest_api_down"