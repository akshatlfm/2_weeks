import ProfileCard from "./ProfileCard";


const profiles = [
    {
      id:1,name:"Akshat",city:"Jaipur"
    },
    {
      id:2,name:"Brian",city:"Delhi"
    },
    {
      id:3,name:"Alice",city:"Mumbai"
    }
]

function Gallery(){
    return(
        <div className="gallery">
            { profiles.map((profile)=>(
                <ProfileCard key={profile.id} name={profile.name} city={profile.city}/>
            ))}
        </div>
    )
}

export default Gallery
