# import os
# import pandas as pd
# from bson import ObjectId
# from app import db
#
# def import_agents_from_csv(file_path):
#     df = pd.read_csv(file_path)
#     agents_collection = db.agents
#
#     for _, row in df.iterrows():
#         agent = {
#             "name": row.get("name"),
#             "email": row.get("email"),
#             "phone": row.get("phone"),
#             "npn": row.get("NPN"),
#             # Add other fields as necessary
#         }
#         agents_collection.update_one(
#             {"npn": row.get("NPN")},
#             {"$set": agent},
#             upsert=True
#         )
#
#     os.remove(file_path)
