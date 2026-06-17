import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Please set GEMINI_API_KEY")


    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()


    client = genai.Client(api_key=api_key)

    messages: list[type.Content] = [types.Content(
        role="user",
        parts=[types.Part(text=args.user_prompt)]
    )]

    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
            config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0
        ),
    )


    if not response.usage_metadata:
        raise RuntimeError("Failed API request. Please try again.")
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if response.function_calls:
        for call in response.function_calls:
            #print(f"Calling function: {call.name}({call.args})")
            function_call_result = call_function(call, args.verbose)
            if not function_call_result.parts:
                raise Exception(f"""
                Error: function "{call.name}({call.args})" result must have a non-empty .parts list.
                """)
            if not function_call_result.parts[0].function_response:
                raise Exception(f"""
                Error: function "{call.name}({call.args})" result should return a FunctionRespose object, not None.
                """)
            if not function_call_result.parts[0].function_response.response: 
                raise Exception(f"""
                Error: function "{call.name}({call.args})" result should return response, not None.
                """)
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

    else:
        print("Response:")
        print(response.text)



if __name__ == "__main__":
    main()
