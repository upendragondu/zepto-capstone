from support_assistant.graph import graph


questions = [
    "How can I get a refund?",
    "Can I cancel my order?",
    "What is the capital of India?"
]


for question in questions:

    print("\n" + "=" * 60)
    print("QUESTION:", question)

    result = graph.invoke({
        "question": question
    })

    print("INTENT:", result["intent"])
    print("ANSWER:", result["answer"])
    print("SOURCES:", result["sources"])
    print("CONFIDENCE:", result["confidence"])