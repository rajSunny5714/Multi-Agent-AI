from agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)


def run_research_pipeline(topic):

    state = {}

    print("=" * 60)
    print("STEP 1 : SEARCH")
    print("=" * 60)

    search_agent = build_search_agent()

    result = search_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"""
Search the web about

{topic}

Return recent trustworthy information.
"""
                )
            ]
        }
    )

    state["search"] = result["messages"][-1].content

    print(state["search"])

    print("\n")
    print("=" * 60)
    print("STEP 2 : READER")
    print("=" * 60)

    reader = build_reader_agent()

    result = reader.invoke(
        {
            "messages": [
                (
                    "user",
                    f"""
Read the most relevant webpage.

Search Results:

{state["search"]}
"""
                )
            ]
        }
    )

    state["reader"] = result["messages"][-1].content

    print(state["reader"][:1000])

    print("\n")
    print("=" * 60)
    print("STEP 3 : WRITER")
    print("=" * 60)

    report = writer_chain.invoke(
        {
            "topic": topic,
            "research": state["search"] + "\n\n" + state["reader"]
        }
    )

    state["report"] = report

    print(report)

    print("\n")
    print("=" * 60)
    print("STEP 4 : CRITIC")
    print("=" * 60)

    feedback = critic_chain.invoke(
        {
            "report": report
        }
    )

    state["feedback"] = feedback

    print(feedback)

    return state


if __name__ == "__main__":

    topic = input("Enter topic : ")

    run_research_pipeline(topic)