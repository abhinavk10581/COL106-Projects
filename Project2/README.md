
---

## 📌 2. Plagiarism Detection Engine — `README.md`

```markdown
# 📄 Plagiarism Detection Engine

A document similarity checker that detects plagiarism using n-gram analysis and custom-built hash tables.

## 🚀 Features

- Tokenizes documents using n-grams
- Computes similarity scores between files
- Custom hash map and set implementation
- Dynamic resizing and rehashing

## 🔬 Techniques Used

- String processing and n-gram generation
- Custom HashMap and HashSet (chained hashing)
- Document comparison using Jaccard similarity

## 🧠 Data Structures

- `HashMap`: With chaining and rehashing
- `HashSet`: Built on top of `HashMap`

## 🧪 Example

```bash
python plagiarism_checker.py file1.txt file2.txt
