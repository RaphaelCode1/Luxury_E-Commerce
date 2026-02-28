from backend import create_app

app = create_app()

print("\n" + "="*50)
print("ALL REGISTERED ROUTES")
print("="*50 + "\n")

with app.app_context():
    for rule in sorted(app.url_map.iter_rules(), key=lambda x: str(x)):
        methods = ','.join(rule.methods - {'HEAD', 'OPTIONS'})
        print(f"{rule.endpoint:30} {methods:10} {rule.rule}")

print("\n" + "="*50)
print(f"Total routes: {len(list(app.url_map.iter_rules()))}")
print("="*50 + "\n")
