# Retrieval-Strategien

## 1. Similarity-basiertes Retrieval
````python
retriever = vector_db.as_retriever(
        search_type="similarity",
         search_kwargs={
             "k": 35,           # Menge
         },  
    )
````

## 2. Schwellenwert-basiertes Retrieval
````python
retriever = vector_db.as_retriever(
    search_type="similarity_score_threshold",
     search_kwargs={
         "k": 35,                  # Menge           
         "score_threshold": 0.45,  # Mindestscore
    },
)
````

## 3. Maximal Marginal Relevance (MMR)
````python
retriever = vector_db.as_retriever(
    search_type="mmr",
     search_kwargs={
     "k":35,                # Menge
     "fetch_k":60,          # Kandidatenpool
     "lambda_mult": 0.15,   # Relevanz / Diversität (Vielfältigkeit)
     },
)
````