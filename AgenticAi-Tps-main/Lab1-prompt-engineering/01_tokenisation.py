import tiktoken


def num_tokens_from_string(string: str, encoding_name: str = "o200k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(string))


encoding = tiktoken.encoding_for_model("gpt-4o")
print("Encoding utilise:", encoding.name)

system_message = """
Analyze the sentiment expressed in the customer review provided in the user message.
Return only: positive or negative.
No explanation needed.
"""

tokens = encoding.encode(system_message)

print("Nombre de tokens du prompt system:", len(tokens))
print("Liste des tokens:", tokens)
print("Reconstruction token par token:")
for token in tokens:
    print(encoding.decode_single_token_bytes(token).decode("utf-8", errors="ignore"), end="")

print("\n")
print("Exemple simple:", num_tokens_from_string("tiktoken is great!"))
