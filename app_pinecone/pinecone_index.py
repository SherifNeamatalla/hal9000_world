import pinecone

pinecone.init(api_key="your_pinecone_api_key")
pinecone.deinit()  # Call this when you're done using Pinecone
