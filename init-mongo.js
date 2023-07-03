db.createUser(
    {
        user: "yakubov",
        pwd: "password",
        roles: [
            {
                role: "readWrite",
                db: "topskill_study_db"
            }
        ]
    }
)