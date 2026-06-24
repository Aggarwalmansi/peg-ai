"""
Golden dataset for PEG AI evaluation.

Each entry is a real test case with a KNOWN correct label.
You will need to fill in / expand these with real examples — the ones
below are starting templates so you can see the shape of the data.

Why this structure:
- `id`: lets you track the same test case across multiple eval runs over time
- `input`: the raw text exactly as your pipeline would receive it
- `expected_label`: ground truth — what the system SHOULD say
- `category`: lets you break down accuracy by category later (this is how
  you find out "it's good at obvious scams but bad at Hinglish" instead of
  just one flat accuracy number)
- `notes`: why this case is hard / what it's testing — useful when you
  revisit this in 3 months and forget why you included it
"""

GOLDEN_SET = [
    # --- OTP Phishing ---
    {
        "id": "otp_scam_001",
        "input": "Your bank account will be blocked. Click here to verify your OTP immediately: bit.ly/xyz123",
        "expected_label": "scam",
        "category": "otp",
        "notes": "Classic OTP phishing, no ambiguity",
    },
    {
        "id": "otp_scam_002",
        "input": "Dear customer, your debit card is suspended. Please share the 6-digit code sent to your mobile to reactivate.",
        "expected_label": "scam",
        "category": "otp",
        "notes": "Asking for OTP directly in message, disguising as 6-digit code",
    },
    {
        "id": "otp_scam_003",
        "input": "We noticed an unauthorized login attempt on your account. Reply with the OTP you just received to cancel it.",
        "expected_label": "scam",
        "category": "otp",
        "notes": "Sense of urgency, asks to reply with OTP",
    },
    {
        "id": "otp_scam_004",
        "input": "Your mobile number will be deactivated in 2 hours. Call customer care at 9876543210 and share your OTP to continue service.",
        "expected_label": "scam",
        "category": "otp",
        "notes": "Telecom scam, urgency + phone number + OTP",
    },
    {
        "id": "otp_scam_005",
        "input": "SBI Alert: Your NetBanking is disabled. To reactivate, click here: http://sbi-reactivate-login.com and authenticate with OTP.",
        "expected_label": "scam",
        "category": "otp",
        "notes": "Bank phishing link requiring OTP",
    },
    {
        "id": "otp_scam_006",
        "input": "Dear user, you have initiated a transaction of Rs.15000. If you did not do this, share the OTP to cancel.",
        "expected_label": "scam",
        "category": "otp",
        "notes": "Reverse psychology scam, asks for OTP to 'cancel'",
    },
    {
        "id": "otp_safe_001",
        "input": "Hey, did you get the OTP for the Netflix login?",
        "expected_label": "safe",
        "category": "otp_hard_negative",
        "notes": "Contains OTP keyword, but casual conversation",
    },
    {
        "id": "otp_safe_002",
        "input": "My OTP is 492014. Please don't share this with anyone.",
        "expected_label": "safe",
        "category": "otp_hard_negative",
        "notes": "Actual OTP message forward or discussion, not a scammer asking for it",
    },
    {
        "id": "otp_safe_003",
        "input": "I didn't receive the OTP yet, can you resend?",
        "expected_label": "safe",
        "category": "otp_hard_negative",
        "notes": "User complaint about OTP",
    },
    {
        "id": "otp_safe_004",
        "input": "The OTP to login to your app is 998822.",
        "expected_label": "safe",
        "category": "otp_hard_negative",
        "notes": "System generated OTP message format",
    },
    {
        "id": "otp_hinglish_safe_001",
        "input": "Bhai OTP bhej de jaldi se, payment karni hai.",
        "expected_label": "safe",
        "category": "hinglish_hard_negative",
        "notes": "Friend asking for OTP, very hard negative. Context is payment between friends, but risky.",
    },
    {
        "id": "otp_hinglish_safe_002",
        "input": "Mera OTP nahi aaya, customer care ko call karna padega kya?",
        "expected_label": "safe",
        "category": "hinglish_hard_negative",
        "notes": "Mentions OTP but is the USER complaining, not a scammer requesting it — tests false positive rate",
    },

    # --- UPI Fraud ---
    {
        "id": "upi_scam_001",
        "input": "Congratulations! You have won Rs.5000 in phonepe scratch card. Enter your UPI PIN to claim your reward.",
        "expected_label": "scam",
        "category": "upi",
        "notes": "UPI PIN to receive money scam",
    },
    {
        "id": "upi_scam_002",
        "input": "Hello I am from Olx. To receive payment for your furniture, open Google Pay and click 'Pay' to authorize my transaction.",
        "expected_label": "scam",
        "category": "upi",
        "notes": "OLX/Marketplace receive money scam",
    },
    {
        "id": "upi_scam_003",
        "input": "Your refund of Rs.1500 has been initiated. Scan this QR code and enter UPI pin to receive the money in your account.",
        "expected_label": "scam",
        "category": "upi",
        "notes": "QR code scam",
    },
    {
        "id": "upi_scam_004",
        "input": "Dear user, electricity bill of Rs.450 is pending. Pay via this UPI link to avoid disconnection at 9:30 PM: upi://pay?pa=scammer@ybl",
        "expected_label": "scam",
        "category": "upi",
        "notes": "Electricity bill disconnection scam",
    },
    {
        "id": "upi_scam_005",
        "input": "Please accept the UPI mandate for your Hotstar subscription renewal. Click here: upi://mandate?pa=hotstar@hdfc",
        "expected_label": "scam",
        "category": "upi",
        "notes": "Fake UPI mandate request",
    },
    {
        "id": "upi_scam_006",
        "input": "Your KYC for Paytm is pending. Send Re.1 via UPI to verify your bank account.",
        "expected_label": "scam",
        "category": "upi",
        "notes": "Small amount transfer scam to verify account",
    },
    {
        "id": "upi_hinglish_scam_001",
        "input": "Sir maine by mistake aapko Rs.5000 send kar diya hai PhonePe par, please mujhe wapas kar do yeh mera medical emergency hai.",
        "expected_label": "scam",
        "category": "hinglish_scam",
        "notes": "Wrong transfer scam, emotional manipulation in Hinglish",
    },
    {
        "id": "upi_safe_001",
        "input": "Please send Rs. 500 to my UPI ID when you get a chance.",
        "expected_label": "safe",
        "category": "upi_hard_negative",
        "notes": "Normal UPI request",
    },
    {
        "id": "upi_safe_002",
        "input": "UPI is down today, can you pay in cash?",
        "expected_label": "safe",
        "category": "upi_hard_negative",
        "notes": "Discussing UPI issues",
    },
    {
        "id": "upi_safe_003",
        "input": "Hey, scan my QR code so I can pay you for lunch.",
        "expected_label": "safe",
        "category": "upi_hard_negative",
        "notes": "Normal QR code usage",
    },
    {
        "id": "upi_safe_004",
        "input": "I sent Re. 1 to test if the UPI ID was correct.",
        "expected_label": "safe",
        "category": "upi_hard_negative",
        "notes": "Testing UPI ID, not a scam",
    },
    {
        "id": "upi_hinglish_safe_001",
        "input": "Maine tujhe 500 UPI kar diye hai, check kar lena.",
        "expected_label": "safe",
        "category": "hinglish_hard_negative",
        "notes": "Hinglish, normal UPI transaction confirmation",
    },

    # --- Bank/KYC Scam ---
    {
        "id": "bank_scam_001",
        "input": "Dear Customer, Your HDFC Bank account will be blocked today. Please click the link to update your PAN Card immediately. http://hdfc-pan-update.com",
        "expected_label": "scam",
        "category": "bank",
        "notes": "Bank KYC phishing link",
    },
    {
        "id": "bank_scam_002",
        "input": "Your credit card points worth Rs.8500 will expire today. Click here to redeem them for cash: http://cc-rewards.com/redeem",
        "expected_label": "scam",
        "category": "bank",
        "notes": "Credit card points scam",
    },
    {
        "id": "bank_scam_003",
        "input": "RBI Alert: Your bank account is under review for suspicious activity. Complete your e-KYC here to avoid account freeze.",
        "expected_label": "scam",
        "category": "bank",
        "notes": "Authority impersonation (RBI)",
    },
    {
        "id": "bank_scam_004",
        "input": "Dear user, your YONO SBI is blocked due to incomplete KYC. Update via this apk file: yono-update.apk",
        "expected_label": "scam",
        "category": "bank",
        "notes": "Malicious APK delivery",
    },
    {
        "id": "bank_scam_005",
        "input": "This is Rahul from your bank's fraud prevention team. We noticed suspicious activity. Can you confirm the last 4 digits of your card so I can secure your account?",
        "expected_label": "scam",
        "category": "bank",
        "notes": "Vishing script",
    },
    {
        "id": "bank_scam_006",
        "input": "Dear HDFC Customer, your PAN is not linked with Aadhaar. Your account will be frozen in 24 hours. Link here: http://pan-aadhaar-link-india.com",
        "expected_label": "scam",
        "category": "bank",
        "notes": "PAN-Aadhaar linking scam",
    },
    {
        "id": "bank_scam_007",
        "input": "Income Tax Dept: Your tax refund of Rs.24,500 has been approved. Please verify your bank details here.",
        "expected_label": "scam",
        "category": "bank",
        "notes": "Tax refund phishing",
    },
    {
        "id": "bank_safe_001",
        "input": "I'm going to the bank today to update my KYC documents.",
        "expected_label": "safe",
        "category": "bank_hard_negative",
        "notes": "Contains KYC and bank keywords",
    },
    {
        "id": "bank_safe_002",
        "input": "My account got blocked because I entered the wrong password too many times.",
        "expected_label": "safe",
        "category": "bank_hard_negative",
        "notes": "Account blocked mention",
    },
    {
        "id": "bank_safe_003",
        "input": "Do you have the link to the official SBI net banking portal?",
        "expected_label": "safe",
        "category": "bank_hard_negative",
        "notes": "Asking for bank link",
    },
    {
        "id": "bank_safe_004",
        "input": "Bank server is down, try doing the NEFT tomorrow.",
        "expected_label": "safe",
        "category": "bank_hard_negative",
        "notes": "Discussing bank servers",
    },
    {
        "id": "bank_safe_005",
        "input": "Is this the right link for the Income Tax portal? eportal.incometax.gov.in",
        "expected_label": "safe",
        "category": "bank_hard_negative",
        "notes": "Legitimate inquiry about govt portal",
    },

    # --- Delivery Scam ---
    {
        "id": "delivery_scam_001",
        "input": "India Post: Your package cannot be delivered due to incomplete address. Please pay Rs.5 redelivery fee here: http://indiapost-track-info.com",
        "expected_label": "scam",
        "category": "delivery",
        "notes": "Postal scam, small fee request",
    },
    {
        "id": "delivery_scam_002",
        "input": "BlueDart: Your parcel is on hold. Update delivery address and pay customs clearance fee of Rs.49: http://bluedart-clearance.net",
        "expected_label": "scam",
        "category": "delivery",
        "notes": "Courier scam, customs fee",
    },
    {
        "id": "delivery_hinglish_scam_001",
        "input": "Sir maine aapko OTP bheja hai delivery confirm karne ke liye, kripya share kare taaki order deliver ho sake",
        "expected_label": "scam",
        "category": "hinglish_scam",
        "notes": "Hinglish, asks for OTP under delivery pretext",
    },
    {
        "id": "delivery_scam_003",
        "input": "Your Amazon order #19283 is cancelled. Click here to claim your refund and enter your card details.",
        "expected_label": "scam",
        "category": "delivery",
        "notes": "Fake order cancellation and refund",
    },
    {
        "id": "delivery_scam_004",
        "input": "Delivery partner couldn't locate your address. Call this number to guide him: +919876543210. He will ask for a verification code.",
        "expected_label": "scam",
        "category": "delivery",
        "notes": "Delivery verification code scam",
    },
    {
        "id": "delivery_scam_005",
        "input": "Swiggy: Your delivery executive met with an accident. Please pay Rs.20 for a replacement executive to deliver your food.",
        "expected_label": "scam",
        "category": "delivery",
        "notes": "Emotional manipulation food delivery scam",
    },
    {
        "id": "delivery_scam_006",
        "input": "Flipkart Big Billion Days: You've won a surprise gift! Pay only Rs.99 delivery charge to claim.",
        "expected_label": "scam",
        "category": "delivery",
        "notes": "Fake e-commerce gift requiring delivery fee",
    },
    {
        "id": "delivery_safe_001",
        "input": "Your Amazon delivery agent is at the gate. Share OTP to receive your order.",
        "expected_label": "safe",
        "category": "delivery_hard_negative",
        "notes": "Legitimate delivery OTP request format",
    },
    {
        "id": "delivery_safe_002",
        "input": "My package is delayed, I'll call customer support.",
        "expected_label": "safe",
        "category": "delivery_hard_negative",
        "notes": "Package delay complaint",
    },
    {
        "id": "delivery_safe_003",
        "input": "Can you track my order? The tracking ID is AW123456789.",
        "expected_label": "safe",
        "category": "delivery_hard_negative",
        "notes": "Tracking ID mention",
    },
    {
        "id": "delivery_hinglish_safe_001",
        "input": "Bhai mera order receive kar lena aur usko OTP bata dena, main meeting mein hu.",
        "expected_label": "safe",
        "category": "hinglish_hard_negative",
        "notes": "Hinglish, sharing OTP for legitimate reason",
    },

    # --- Job Scam ---
    {
        "id": "job_scam_001",
        "input": "Work from home and earn Rs.5000 daily! Just like YouTube videos. Click here to register and pay Rs.500 onboarding fee.",
        "expected_label": "scam",
        "category": "job",
        "notes": "Task-based scam, upfront fee",
    },
    {
        "id": "job_scam_002",
        "input": "You have been selected for Data Entry job at Wipro. Salary: 45k/month. Send your Aadhar, PAN and Rs.1000 registration fee to hr@wipro-jobs-portal.com",
        "expected_label": "scam",
        "category": "job",
        "notes": "Fake job offer, document collection and fee",
    },
    {
        "id": "job_scam_003",
        "input": "Amazon Hiring! Part-time remote work. Click link to join Telegram group and start earning by rating products.",
        "expected_label": "scam",
        "category": "job",
        "notes": "Telegram task scam funnel",
    },
    {
        "id": "job_scam_004",
        "input": "Earn money by simply liking Instagram posts! Message our manager on WhatsApp at +918888888888 to start.",
        "expected_label": "scam",
        "category": "job",
        "notes": "Social media liking scam",
    },
    {
        "id": "job_scam_005",
        "input": "Google Maps Review Job: Earn Rs.150 per review! Add our recruiter on Telegram to start working immediately.",
        "expected_label": "scam",
        "category": "job",
        "notes": "Map review task scam",
    },
    {
        "id": "job_scam_006",
        "input": "Urgent hiring for online typists. No experience required. Pay Rs.200 for typing test.",
        "expected_label": "scam",
        "category": "job",
        "notes": "Fake typing job with test fee",
    },
    {
        "id": "job_safe_001",
        "input": "Hey, I saw an opening for a software engineer at your company. Can you refer me?",
        "expected_label": "safe",
        "category": "job_hard_negative",
        "notes": "Legitimate job inquiry",
    },
    {
        "id": "job_safe_002",
        "input": "I got a job offer from Infosys today! So excited.",
        "expected_label": "safe",
        "category": "job_hard_negative",
        "notes": "Job offer mention",
    },
    {
        "id": "job_safe_003",
        "input": "Please review my resume for the data analyst role.",
        "expected_label": "safe",
        "category": "job_hard_negative",
        "notes": "Resume review request",
    },
    {
        "id": "job_safe_004",
        "input": "The interview is scheduled for tomorrow at 10 AM over Google Meet.",
        "expected_label": "safe",
        "category": "job_hard_negative",
        "notes": "Interview scheduling",
    },

    # --- Investment Scam ---
    {
        "id": "investment_scam_001",
        "input": "Join our VIP stock trading group. Assured 200% return in 1 month. Invest Rs.10000 now to start. Click to join Telegram channel.",
        "expected_label": "scam",
        "category": "investment",
        "notes": "Stock tips scam, guaranteed returns",
    },
    {
        "id": "investment_scam_002",
        "input": "Your crypto wallet is compromised. Transfer your BTC to this secure address immediately to protect your funds.",
        "expected_label": "scam",
        "category": "investment",
        "notes": "Crypto transfer scam",
    },
    {
        "id": "investment_scam_003",
        "input": "Make money fast with this new crypto token! Pre-sale is live. Connect your Metamask wallet here to buy: http://fake-token-sale.com",
        "expected_label": "scam",
        "category": "investment",
        "notes": "Crypto presale phishing",
    },
    {
        "id": "investment_scam_004",
        "input": "Invest in high-yield mutual funds. Guaranteed double returns in 6 months. Download our trading app from this link to start.",
        "expected_label": "scam",
        "category": "investment",
        "notes": "Fake investment app",
    },
    {
        "id": "investment_hinglish_scam_001",
        "input": "Sir, I have a guaranteed stock tip for tomorrow. Buy this penny stock. Pay 5000 rs for premium tips.",
        "expected_label": "scam",
        "category": "hinglish_scam",
        "notes": "Stock tip scam in Hinglish",
    },
    {
        "id": "investment_safe_001",
        "input": "I bought some shares of Reliance today. Let's see how they perform.",
        "expected_label": "safe",
        "category": "investment_hard_negative",
        "notes": "Discussing stock purchase",
    },
    {
        "id": "investment_safe_002",
        "input": "Mutual funds are subject to market risks. Please read the offer document carefully before investing.",
        "expected_label": "safe",
        "category": "investment_hard_negative",
        "notes": "Standard mutual fund disclaimer",
    },
    {
        "id": "investment_safe_003",
        "input": "Did you check the crypto market today? Bitcoin is up by 5%.",
        "expected_label": "safe",
        "category": "investment_hard_negative",
        "notes": "Crypto market discussion",
    },

    # --- Rewards/Lottery Scam ---
    {
        "id": "reward_scam_001",
        "input": "Congratulations! Your mobile number won the KBC lottery of Rs.25 Lakhs. Call the manager at +917777777777 to claim it.",
        "expected_label": "scam",
        "category": "reward",
        "notes": "Classic KBC lottery scam",
    },
    {
        "id": "reward_scam_002",
        "input": "Jio 5G Launch offer! Get 3 months of free unlimited data. Click here to activate now: http://jio-free-recharge.com",
        "expected_label": "scam",
        "category": "reward",
        "notes": "Free recharge scam",
    },
    {
        "id": "reward_scam_003",
        "input": "You have been selected for a free iPhone 15 Pro Max giveaway. Just pay Rs.250 for shipping and handling.",
        "expected_label": "scam",
        "category": "reward",
        "notes": "Giveaway shipping fee scam",
    },
    {
        "id": "reward_scam_004",
        "input": "Dear customer, your reward points are expiring. Click the link to claim a free gift from our catalog.",
        "expected_label": "scam",
        "category": "reward",
        "notes": "Expiring reward points scam",
    },
    {
        "id": "reward_safe_001",
        "input": "I just redeemed my credit card points for an Amazon gift card.",
        "expected_label": "safe",
        "category": "reward_hard_negative",
        "notes": "Legitimate reward redemption mention",
    },
    {
        "id": "reward_safe_002",
        "input": "Do we get free shipping if the order is over Rs.500?",
        "expected_label": "safe",
        "category": "reward_hard_negative",
        "notes": "Asking about free shipping",
    },

    # --- Clear Negative (General Chit Chat) ---
    {
        "id": "clear_negative_001",
        "input": "Hey, are we still meeting for lunch tomorrow at 1pm?",
        "expected_label": "safe",
        "category": "clear_negative",
        "notes": "Completely benign, sanity check",
    },
    {
        "id": "clear_negative_002",
        "input": "Can you send me the grocery list?",
        "expected_label": "safe",
        "category": "clear_negative",
        "notes": "Benign request",
    },
    {
        "id": "clear_negative_003",
        "input": "Happy Birthday! Have a great day ahead.",
        "expected_label": "safe",
        "category": "clear_negative",
        "notes": "Greeting",
    },
    {
        "id": "clear_negative_004",
        "input": "I'll be reaching the station in 10 minutes.",
        "expected_label": "safe",
        "category": "clear_negative",
        "notes": "Update on location",
    },

    # --- Hinglish Safe (Chit Chat) ---
    {
        "id": "hinglish_safe_002",
        "input": "Bhai kaha hai tu? Kab tak aayega?",
        "expected_label": "safe",
        "category": "hinglish_safe",
        "notes": "Hinglish chit chat",
    },
    {
        "id": "hinglish_safe_003",
        "input": "Mera internet kaam nahi kar raha hai, customer care ka number hai kya tere paas?",
        "expected_label": "safe",
        "category": "hinglish_safe",
        "notes": "Hinglish support request",
    },
    {
        "id": "hinglish_safe_004",
        "input": "Account mein paise aa gaye hai, thanks!",
        "expected_label": "safe",
        "category": "hinglish_safe",
        "notes": "Hinglish payment confirmation",
    },

    # --- Edge Cases ---
    {
        "id": "edge_case_001",
        "input": "",
        "expected_label": "safe",
        "category": "edge_case",
        "notes": "Empty input — should not crash, should not flag",
    },
    {
        "id": "edge_case_002",
        "input": "ok",
        "expected_label": "safe",
        "category": "edge_case",
        "notes": "Minimal input, no signal either way",
    },
    {
        "id": "edge_case_003",
        "input": "scam",
        "expected_label": "safe",
        "category": "edge_case",
        "notes": "Just the word scam, lacks actual scam intent",
    },
    {
        "id": "edge_case_004",
        "input": "123456",
        "expected_label": "safe",
        "category": "edge_case",
        "notes": "Just numbers, could be OTP but no context",
    },
]

if __name__ == "__main__":
    from collections import Counter
    cats = Counter(item["category"] for item in GOLDEN_SET)
    print(f"Total cases: {len(GOLDEN_SET)}")
    print(f"By category: {dict(cats)}")