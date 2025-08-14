# Correct OpenAI API Examples

## 🔧 Correct Curl Command Format

The correct curl command for OpenAI Chat API is:

```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "user", "content": "write a haiku about ai"}
    ],
    "max_tokens": 50
  }'
```

## ❌ Issues with Your Original Command

Your original command had these problems:
1. **Wrong endpoint**: `/v1/responses` → should be `/v1/chat/completions`
2. **Wrong format**: `"input"` → should be `"messages"` array
3. **Invalid parameter**: `"store": true` → not needed for basic calls

## ✅ PowerShell Version

For Windows PowerShell, use this format:

```powershell
$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer YOUR_API_KEY"
}

$body = @{
    model = "gpt-4o-mini"
    messages = @(@{role = "user"; content = "write a haiku about ai"})
    max_tokens = 50
} | ConvertTo-Json -Depth 3

$response = Invoke-RestMethod -Uri "https://api.openai.com/v1/chat/completions" -Method Post -Headers $headers -Body $body
$response.choices[0].message.content
```

## 🚨 Current Issue: Quota Exceeded

Both your API keys are showing "insufficient_quota" error. To fix this:

1. **Add billing information** at: https://platform.openai.com/account/billing
2. **Add a payment method** (credit/debit card)
3. **Set a usage limit** for safety (e.g., $10/month)
4. **Check your usage** at: https://platform.openai.com/usage

## 💰 Cost Information

- **gpt-4o-mini**: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- **gpt-3.5-turbo**: ~$0.50 per 1M input tokens, ~$1.50 per 1M output tokens
- **For testing**: $5 will give you thousands of interactions

Your API keys work - you just need to set up billing!
