

function ProfileCard({name,city}){
    return(
        <div className="card">
            <h2 className="card-name">{name}</h2>
            <p className="card-city">{city}</p>
        </div>
    )
}

export default ProfileCard