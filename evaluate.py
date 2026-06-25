from src.generator import generate_answer
import json

test_cases = [
    {
        "question": "What is the basic structure doctrine?",
        "keywords": ["supremacy", "constitution", "separation of powers", "secular", "federal", "democratic"]
    },
    {
        "question": "Can Parliament amend fundamental rights?",
        "keywords": ["article 368", "amend", "basic structure", "kesavananda", "parliament"]
    },
    {
        "question": "What protections does Article 21 provide?",
        "keywords": ["personal liberty", "life", "article 19", "procedure", "narrow"]
    },
    {
        "question": "What did the Maneka Gandhi case decide about personal liberty and procedure?",
        "keywords": ["article 21", "personal liberty", "procedure", "passport", "right to travel", "audi alteram partem", "natural justice"]
    },
    {
        "question": "What did the court say about freedom of speech?",
        "keywords": ["article 19", "freedom", "speech", "expression", "restriction"]
    }
]

def evaluate_faithfulness(answer, sources):
    source_text = " ".join([s.page_content.lower() for s in sources])
    answer_sentences = [s.strip() for s in answer.split(".") if len(s.strip()) > 20]
    grounded = 0
    for sentence in answer_sentences:
        words = sentence.lower().split()
        meaningful_words = [w for w in words if len(w) > 4]
        matches = sum(1 for w in meaningful_words if w in source_text)
        if len(meaningful_words) > 0 and matches / len(meaningful_words) > 0.3:
            grounded += 1
    return grounded / len(answer_sentences) if answer_sentences else 0

def evaluate_answer_relevancy(question, answer, keywords):
    answer_lower = answer.lower()
    question_words = [w.lower() for w in question.split() if len(w) > 3]
    keyword_hits = sum(1 for k in keywords if k.lower() in answer_lower)
    question_hits = sum(1 for w in question_words if w in answer_lower)
    keyword_score = keyword_hits / len(keywords) if keywords else 0
    question_score = question_hits / len(question_words) if question_words else 0
    return (keyword_score + question_score) / 2

def evaluate_context_precision(question, sources, keywords):
    relevant_chunks = 0
    for source in sources:
        chunk_lower = source.page_content.lower()
        hits = sum(1 for k in keywords if k.lower() in chunk_lower)
        if hits >= 1:
            relevant_chunks += 1
    return relevant_chunks / len(sources) if sources else 0

print("Running Legal AI Evaluation")
print("=" * 50)

all_faithfulness = []
all_relevancy = []
all_precision = []
results = []

for case in test_cases:
    print(f"\nQ: {case['question']}")
    answer, sources = generate_answer(case['question'])
    
    faith = evaluate_faithfulness(answer, sources)
    relev = evaluate_answer_relevancy(case['question'], answer, case['keywords'])
    prec  = evaluate_context_precision(case['question'], sources, case['keywords'])
    
    all_faithfulness.append(faith)
    all_relevancy.append(relev)
    all_precision.append(prec)
    
    results.append({
        "question": case['question'],
        "answer": answer[:200],
        "faithfulness": round(faith, 4),
        "answer_relevancy": round(relev, 4),
        "context_precision": round(prec, 4)
    })
    
    print(f"Faithfulness:      {faith:.4f}")
    print(f"Answer Relevancy:  {relev:.4f}")
    print(f"Context Precision: {prec:.4f}")

print("\n" + "=" * 50)
print("FINAL RESULTS")
print("=" * 50)
print(f"Mean Faithfulness:      {sum(all_faithfulness)/len(all_faithfulness):.4f}")
print(f"Mean Answer Relevancy:  {sum(all_relevancy)/len(all_relevancy):.4f}")
print(f"Mean Context Precision: {sum(all_precision)/len(all_precision):.4f}")

with open("evaluation_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nResults saved to evaluation_results.json")