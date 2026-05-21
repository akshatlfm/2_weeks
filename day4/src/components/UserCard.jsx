
function UserCard({name,email}){
    return(
        <div className="card">
            <p>{name}</p>
            <p>{email}</p>
        </div>
          
    )
}

export default UserCard;