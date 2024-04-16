def following(userID, db):
    # get following list

    try:
        with db.cursor() as cursor:
            query = 'SELECT Friends FROM Relationship WHERE UserID=%s'

            cursor.execute(query, userID)

            foll = cursor.fetchall()
            foll = foll.split(',')

        return foll
    except Exception as e:
        print(e)
        return False
