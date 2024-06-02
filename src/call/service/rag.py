from langchain.chains import RetrievalQA

from common.dependencies import get_llm, get_retriever

qa = RetrievalQA.from_chain_type(
    llm=get_llm(),  # model from Huggingface Endpoint
    chain_type="stuff",  # Chain type to use for QA
    retriever=get_retriever(),  # Retriever object for retrieving relevant documents
)

## Example usage
# if __name__ == "__main__":
#
#     query_1 = """
#     Apa saja yang nasabah harus lakukan dalam alur layanan permohonan?
#     """
#
#     # Invoke the QA model with the input query and retrieve the result
#     result = qa.invoke(query_1)['result']
#
#     # Print the result
#     print(result)
