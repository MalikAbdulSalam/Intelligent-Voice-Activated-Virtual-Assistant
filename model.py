from transformers import AutoModelForCausalLM, AutoTokenizer
def distilgpt2_model(asr_text):
    print("inside")
    # Example usage
    # asr_text = "Do you have any book recommendations?"  # Replace with ASR text
    response = generate_response(asr_text)
    print("Chatbot Response:", response)
    return response


def generate_response(asr_text):
    # Load DistilGPT-2, a much smaller and efficient model
    model_name = "distilgpt2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    # Set the EOS token as the padding tokenfy
    tokenizer.pad_token = tokenizer.eos_token


    inputs = tokenizer(asr_text, return_tensors="pt", padding=True)
    attention_mask = inputs['attention_mask']

    # Generate response with better control over length and repetition
    response_ids = model.generate(
        inputs['input_ids'],
        attention_mask=attention_mask,
        max_length=50,        # Set max length to a more reasonable value
        min_length=10,        # Ensure a minimum length for the response
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=3,  # Prevent repetitive responses
        num_return_sequences=1,  # Get a single response
    )

    response = tokenizer.decode(
        response_ids[:, inputs['input_ids'].shape[-1]:][0],
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False
    )
    return response

def llama(text):
    model_name = "meta-llama/Llama-2-7b-chat-hf"  # Adjust this depending on model size
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model.generate(inputs.input_ids, max_length=100)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response






