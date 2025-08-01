import string
import math
import time
import itertools

# Common weak passwords
common_passwords = [
    "123456", "password", "123456789", "12345678", "qwerty", "abc123",
    "password1", "111111", "123123", "admin", "letmein", "welcome"
]

def estimate_entropy(password):
    charset = 0
    if any(c.islower() for c in password): charset += 26
    if any(c.isupper() for c in password): charset += 26
    if any(c.isdigit() for c in password): charset += 10
    if any(c in string.punctuation for c in password): charset += len(string.punctuation)
    return round(len(password) * math.log2(charset), 2) if charset else 0

def estimate_crack_time(entropy):
    guesses = 2 ** entropy
    guesses_per_second = 1_000_000_000
    return guesses / guesses_per_second

def format_time(seconds):
    if seconds < 60: return f"{int(seconds)} seconds"
    elif seconds < 3600: return f"{int(seconds // 60)} minutes"
    elif seconds < 86400: return f"{int(seconds // 3600)} hours"
    elif seconds < 31536000: return f"{int(seconds // 86400)} days"
    else: return f"{int(seconds // 31536000)} years"

def check_password_strength(password):
    score = 0
    feedback = []

    if password.lower() in common_passwords:
        return "❌ Very Weak (Common Password)", feedback, 0

    if len(password) < 8:
        feedback.append("🔸 Use at least 8 characters.")
    else:
        score += 1

    if any(c.islower() for c in password): score += 1
    else: feedback.append("🔸 Add lowercase letters.")

    if any(c.isupper() for c in password): score += 1
    else: feedback.append("🔸 Add uppercase letters.")

    if any(c.isdigit() for c in password): score += 1
    else: feedback.append("🔸 Add numbers.")

    if any(c in string.punctuation for c in password): score += 1
    else: feedback.append("🔸 Add special characters.")

    # Determine strength label
    if score <= 2:
        strength = "⚠️ Weak"
    elif score == 3:
        strength = "🟡 Moderate"
    elif score == 4:
        strength = "🟢 Strong"
    else:
        strength = "🟢🔒 Very Strong"

    entropy = estimate_entropy(password)
    crack_time = estimate_crack_time(entropy)

    return strength, feedback, crack_time

def brute_force_crack(password):
    characters = string.ascii_letters + string.digits + string.punctuation
    attempts = 0
    start = time.time()

    for length in range(1, 6):  # Max 5 chars
        for guess in itertools.product(characters, repeat=length):
            attempts += 1
            guess_str = ''.join(guess)
            if guess_str == password:
                end = time.time()
                return guess_str, attempts, round(end - start, 2)

    return None, attempts, -1

# ==== Main Program ====
if __name__ == "__main__":
    print("\n🔐 SecurePass Analyzer")
    password = input("Enter a password to analyze: ")

    print("\n🔎 Checking strength...")
    strength, feedback, crack_seconds = check_password_strength(password)

    print(f"\nPassword Strength: {strength}")
    if feedback:
        print("Suggestions:")
        for item in feedback:
            print(item)
    else:
        print("✅ Your password meets all strength criteria.")

    print(f"\nEntropy: {estimate_entropy(password)} bits")
    print(f"Estimated time to crack (brute-force): {format_time(crack_seconds)}")

    if len(password) <= 5:
        print("\n🧪 Simulating brute-force attack...")
        result, attempts, time_taken = brute_force_crack(password)
        if result:
            print(f"✅ Password cracked in {attempts} attempts")
            print(f"⏱️ Time taken: {time_taken} seconds")
        else:
            print("❌ Could not crack password (too long or complex)")
    else:
        print("\n⚠️ Skipping brute-force simulation — password too long to simulate.")
