> **Vedic Mastery Study - API Access Protocol v1.0**

This protocol governs access to the auto-generated Supabase APIs.

1.  **Public Access**: The `anon` key can be used for read-only access to public data (e.g., verses, translations).
2.  **Service Role Access**: The `service_role` key is for administrative tasks only and must never be exposed in client-side code.
3.  **Row-Level Security (RLS)**: RLS policies will be implemented to restrict access to sensitive data.
4.  **API Documentation**: The auto-generated API documentation in the Supabase dashboard is the single source of truth.
