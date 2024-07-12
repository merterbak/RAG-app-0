class User:
    def __init__(self, username):
        self.username = username
        self.llm = "gpt-3.5-turbo"
        self.embedder = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"