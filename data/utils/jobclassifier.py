from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


class JobClassifier:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")

        # Load the tokenizer and model
        self.model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")

        # Set up the pipeline
        self.hf_pipeline = pipeline("text2text-generation", model=self.model, tokenizer=self.tokenizer)

        # Wrap the pipeline in LangChain
        self.llm = HuggingFacePipeline(pipeline=self.hf_pipeline)

        # Define the prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["job_title"],
            template=(
                "Classify the following job title into its respective domain. "
                "You must choose one from the domains:\n"
                "Web Development, Software Development, Data Analytics, IT & Networking, Project Management & Administration, "
                "Digital Marketing, Design, Android Development, Testing & Support.\n"
                "Count product manager as Project Management & Administration."
                "And count Backend Development or Frontend Development as Web Development.\n\n"
                "Job Title: {job_title}\n"
                "Domain:"
            )
        )

        # Create the chain
        self.classification_chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    def classify(self, job_title):
        response = self.classification_chain.run(job_title=job_title)
        return(str(response))


# job_title = "Head of Function - Software Operation (AGM/DGM/GM)"
# response = classification_chain.run(job_title=job_title)
# print(f"Domain for '{job_title}': {response}")

