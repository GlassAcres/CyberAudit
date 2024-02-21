from pluginlab_admin import App

class PluginLabHandler:
    def __init__(self, secret_key: str, plugin_id: str, message_handler):
        print(f"[INFO] Initializing PluginLabHandler with plugin_id: {plugin_id}")
        self.app = App(secret_key=secret_key, plugin_id=plugin_id)
        self.auth = self.app.get_auth()
        self.message_handler = message_handler

    def get_token_from_request(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1] 
            print(f"[INFO] Token retrieved from request: {token}")
            return token
        print("[WARNING] No token found in request")
        return None

    def get_user_data_from_token(self, token: str):
        try:
            print(f"[INFO] Verifying token: {token} using plugin_id: {self.app.plugin_id}")
            verified_token = self.auth.verify_token(token)
            print(f"[INFO] Token verified successfully: {verified_token}")
            
            uid = verified_token.uid  # Accessing the uid attribute
            print(f"[INFO] UID retrieved: {uid}")
            
            member = self.auth.get_member_by_id(uid)
            print(f"[INFO] Member details retrieved: {member}")
            
            identities = self.auth.get_member_identities(uid)
            print(f"[INFO] Member identities retrieved: {identities}")
            
            if identities.github:
                github_access_token = identities.github.access_token
            else:
                github_access_token = None  
            
            user_data = {
                "ID" : member.id,
                "email": member.auth.email,
                "name": member.name,
                "given_name": member.given_name,
                "family_name": member.family_name,
                "plan_id": verified_token.user.plan_id,
                "price_id": verified_token.user.price_id,
                "github_token": github_access_token
            }
            print(f"[INFO] User data retrieved: {user_data}")
            return user_data, None
        except Exception as e:
            print(f"[ERROR] Exception occurred while getting user data from token: {e}")
            return None, f"An error occurred: {str(e)}"

