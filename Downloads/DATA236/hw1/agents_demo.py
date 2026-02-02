import json
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

SCHEMA = {
    "type": "object",
    "properties": {
        "tags": {"type": "array", "items": {"type": "string"}, "minItems": 3, "maxItems": 3},
        "summary": {"type": "string"}
    },
    "required": ["tags", "summary"],
    "additionalProperties": False
}

llm = ChatOllama(model="smollm:1.7b", temperature=0, format=SCHEMA)

def run_agents(title, content):
    planner_agent = [SystemMessage(content=("""You are supposed to generate
        metadata for a blog post. Return ONLY JSON that matches the provided schema.
        NO code. The one-sentence summary must be less than or equal to 25 words and
        it should paraphrase the blog content without copying any phrases verbatim.
        IMPORTANT: The summary must NOT contain the title text, must NOT start with the title,
        and must NOT restate the title.
        Example: If the title is 'How to Bake a Cake',
        the summary should be 'Step-by-step guide to baking delicious cakes at home.'""")),
        HumanMessage(content=f"""Generate 3 topical tags based on the {title}and provide a one-sentence summary
        based on the {content} that has a maximum of 25 words Exclude the title from the summary.""")]

    planner_output = llm.invoke(planner_agent).content
    planner = json.loads(planner_output)
    print("Planner Output:", planner)

    reviewer_agent = [SystemMessage(content=("""Review the planner output to ensure that
        the tags are relevant and the one-sentence summary should be less than or equal to 25 words. The summary
        must NOT contain the title text, must NOT start with the title, and must NOT restate the title. Do NOT
        copy paste the content verbatim in the summary. If any of these conditions are not met, fix them.""")),
        HumanMessage(content=json.dumps({"title": title, "content": content, "draft": planner}))]

    reviewer_output = llm.invoke(reviewer_agent).content
    reviewer = json.loads(reviewer_output)
    print("Reviewer Output:", reviewer)

    finalizer_agent = [SystemMessage(content=("""Make sure that the output is strictly JSON and adheres
        to the schema""")),
        HumanMessage(content=json.dumps({"draft": reviewer}))]

    finalizer_output = llm.invoke(finalizer_agent).content
    finalizer = json.loads(finalizer_output)
    print("Final Output:", finalizer)

    print("\nFinal JSON:")
    print(json.dumps(finalizer, indent=2))

if __name__ == "__main__":
    blog_title = "The Rise of AI Music: When Code Meets Creativity"
    blog_content = ("""AI music is changing the way we create and experience sound. By using machine learning, AI can analyze thousands of songs, understand patterns in melody and rhythm, and generate entirely new music in seconds. What once took hours in a studio can now start with a simple prompt.

For artists, AI is less about replacement and more about collaboration. Musicians use AI tools to spark ideas, explore new genres, or build background tracks faster than ever. For listeners, it means more personalized music—soundtracks that adapt to moods, moments, or even real-time activities.

As AI music continues to evolve, it raises exciting questions about creativity and authorship. One thing is clear: the future of music won’t be just human or machine—it’ll be a blend of both, creating sounds we’ve never heard before.
""")
    run_agents(blog_title, blog_content)
