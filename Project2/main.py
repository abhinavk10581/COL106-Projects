from plagiarism_engine import PlagiarismEngine

def main():
    print("=== Plagiarism Detection Engine Test ===")
    
    # Initialize engine with 3-grams
    try:
        engine = PlagiarismEngine("Chain", (257, 101), 3)
        print("Engine initialized successfully")
    except Exception as e:
        print(f"Failed to initialize engine: {e}")
        return
    
    # Example usage with sample documents
    docs = {
        "doc1": "this is a sample document for testing plagiarism detection".split(),
        "doc2": "this document is a test sample for detecting plagiarism in text".split(), 
        "doc3": "completely different content with no overlap at all here".split(),
        "doc4": "this is a sample document".split()  # shorter document
    }
    
    # Add documents to engine
    print("\n=== Adding Documents ===")
    for title, words in docs.items():
        try:
            engine.add_document(title, words)
            count = engine.get_distinct_count(title)
            print(f"Added {title}: {len(words)} words, {count} distinct n-grams")
        except Exception as e:
            print(f"Error adding {title}: {e}")
    
    print("\n=== Pairwise Comparisons ===")
    pairs = [("doc1", "doc2"), ("doc1", "doc3"), ("doc1", "doc4"), ("doc2", "doc3")]
    for t1, t2 in pairs:
        score = engine.compare_pair(t1, t2)
        print(f"Similarity {t1}-{t2}: {score:.4f}")
    
    print("\n=== Most Similar ===")
    for title in ["doc1", "doc2"]:
        best, score = engine.find_most_similar(title)
        if best:
            print(f"Most similar to {title}: {best} (score: {score:.4f})")
        else:
            print(f"No comparison possible for {title}")
    
    print("\n=== Pairs Above Threshold 0.1 ===")
    pairs = engine.report_similar_pairs(0.1)
    if pairs:
        for t1, t2, score in pairs:
            print(f"{t1} -- {t2}: {score:.4f}")
    else:
        print("No pairs found above threshold 0.1")

if __name__ == "__main__":
    main()