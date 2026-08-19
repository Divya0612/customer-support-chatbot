from google.genai import types

TOOL_DEFINITIONS = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="track_order",
                description="Track the current status, location, and delivery estimate of a customer's order.",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "order_id": types.Schema(
                            type="STRING",
                            description="The order ID provided by the customer, e.g. ORD-1001",
                        )
                    },
                    required=["order_id"],
                ),
            ),
            types.FunctionDeclaration(
                name="cancel_order",
                description="Cancel a customer's order. Only possible if the order is still in processing stage.",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "order_id": types.Schema(
                            type="STRING",
                            description="The order ID the customer wants to cancel",
                        )
                    },
                    required=["order_id"],
                ),
            ),
            types.FunctionDeclaration(
                name="check_refund_status",
                description="Check the refund status for a customer's returned or cancelled order.",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "order_id": types.Schema(
                            type="STRING",
                            description="The order ID to check refund status for",
                        )
                    },
                    required=["order_id"],
                ),
            ),
            types.FunctionDeclaration(
                name="connect_human_agent",
                description="Escalate the conversation and connect the customer to a human support agent. Use this when the customer is frustrated, has a complex issue, or explicitly asks for a human.",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={},
                ),
            ),
            types.FunctionDeclaration(
                name="search_knowledge_base",
                description="Search the knowledge base for information about company policies, shipping timelines, refund and return rules, FAQs, payment methods, and general store information. Use this for any general question not related to a specific order.",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "query": types.Schema(
                            type="STRING",
                            description="The search query to find relevant information from the knowledge base",
                        )
                    },
                    required=["query"],
                ),
            ),
        ]
    )
]
