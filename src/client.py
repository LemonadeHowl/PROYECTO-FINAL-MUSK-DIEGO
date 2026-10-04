class Client:
   def __init__(self, client_id, name: str, country:str, signup_date:str):
      self.client_id = int(client_id)
      self.name = str(name)
      self.country = str(country)
      self.signup_date = str(signup_date)

   def to_dict(self):
      return {
         'client_id': self.client_id,
         'name': self.name,
         'country': self.country,
         'signup_date': self.signup_date,
      }
