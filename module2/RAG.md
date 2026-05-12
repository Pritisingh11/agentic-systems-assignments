Q1. Why did the plain ChatGPT-style chatbot give wrong answers?
The plain chatbot gave wrong answers because it had no direct access to ShopEase’s internal policy documents. It was answering from general language patterns learned during training, not from ShopEase’s real rules. That means it could miss recent policy updates too, because its knowledge is static and may be outdated. When the model does not know the exact answer, it may hallucinate — this means it produces a confident-sounding answer that is not actually true. For example, the chatbot might tell a customer, “refunds are processed in 3 days,” even though ShopEase’s Refund Timelines Policy says refunds take 7 working days after the returned item is received. In a support setting, that kind of made-up answer causes confusion, bad expectations, and extra support tickets.


Q2. What should the new assistant "read from" to give correct answers?
Returns & Replacements Policy : answers questions about return windows, damaged items, and replacement eligibility.
Refund Timelines Policy : explains how long refunds take and when the clock starts.
Shipping & Delivery Guide : answers questions about delivery times, delays, and lost parcels.
Warranty & Repairs Terms : covers warranty duration, repair coverage, and exclusions.
Order Cancellation Rules : explains when an order can be cancelled and what happens after dispatch.


Q3. Walk through the 4-step RAG flow for one realistic ShopEase customer question.
Customer question: “I received a damaged mixer-grinder 5 days ago. Can I still get a replacement?”
1) Query

This exact question is sent to the assistant.
2) Retrieve

The system searches ShopEase’s policy documents and finds the Returns & Replacements Policy. A matching chunk might say:

“Damaged or defective items are eligible for replacement if reported within 7 days of delivery.

Customers must upload a photo of the damage and keep the original packaging.

Replacement is subject to stock availability.”

3) Context

That policy chunk is placed into the prompt alongside the customer’s question, so the LLM sees both the question and the correct rule at the same time.

4) Generate

Using the retrieved policy text, the assistant answers:

“Yes , if you report it within 7 days of delivery, your mixer-grinder is eligible for replacement. Please upload a photo of the damage and keep the original packaging. If the item is in stock, ShopEase can arrange a replacement.”



------------------------------------
RAG
1.User Query ->
2.Retriver (top relevant doc) ->
3.Generator (LLM) -> response
---
Main component of RAG system
Knowledge source (doc pdf image etc) -> chunks(large doc to smaller for better processing) -> Embeddings(numerical represntation of data) -> Vector database -> LLM (brain)
