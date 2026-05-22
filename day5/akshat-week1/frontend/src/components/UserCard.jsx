
function UserCard({title,userId}){
    return(
        <div className="card">
            
            <p>{userId}</p>
             <p>{title}</p>

        </div>
          
    )
}

export default UserCard;