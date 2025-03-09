from supabase import create_client, Client

SUPABASE_URL = "supabase_url"
SUPABASE_KEY = "your_key"

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def store_(author, text): #adding message
    supabase.table("messages").insert({"author": author, "text_content": text}).execute()
    print(f"Message stored: {author} - {text}")

def store_1(author, text):
    supabase.table("knowledge").insert({"author": author, "text": text}).execute()
    print(f"Message stored: {author} - {text}")

def delete_(message_id): #deleting message
    response = supabase.table("messages").delete().match({"id": message_id}).execute()
    print(f"Deleted message with ID: {message_id}")
    return response

def merge_(author, message_ids=None): #merging messages
    query = supabase.table("messages").select("id, text_content").eq("author", author)
    if message_ids:
        query = query.in_("id", message_ids)
    response = query.execute()
    messages = response.data
    if not messages:
        print("No messages found to merge.")
        return
    merged_text = "".join(msg["text_content"] for msg in messages)
    first_message_id = messages[0]["id"]
    supabase.table("messages").update({"text_content": merged_text}).eq("id", first_message_id).execute()
    for msg in messages[1:]:
        supabase.table("messages").delete().eq("id", msg["id"]).execute()
    return(f"`Merged` {len(messages)} messages into ID {first_message_id}")

def update_(author, upi_id): #updating upi
    result = supabase.table("credential").select("author").eq("author", author).execute()
    if result.data:
        supabase.table("credential").update({"upi_id": upi_id}).eq("author", author).execute()
    else:
        supabase.table("credential").insert({"author": author, "upi_id": upi_id}).execute()
    return(f"`Notification:` UPI ID updated for {author}")

def get_tables(tablename = "messages"):
    all_rows =[]
    """Fetch and print all rows from messages and credential tables."""
    messages = supabase.table(f"{tablename}").select("*").execute()
    for row in messages.data:
        all_rows+=[row]
    return all_rows

def store_r(author, remainder_time, message):
    supabase.table("reminders").insert({
        "author": str(author), 
        "time": remainder_time,  # Type/config - "DD-MM-YYYY HH:MM"
        "message": message,
        "notified": False  
    }).execute()

def get_ar():
    return supabase.table("reminders").select("*").execute().data

def delete_r(reminder_id):
    supabase.table("reminders").delete().eq("id", reminder_id).execute()

def notified_r(reminder_id):
    supabase.table("reminders").update({"notified": True}).eq("id", reminder_id).execute()


