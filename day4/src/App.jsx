import { useEffect, useState } from "react";
import UserCard from "./components/UserCard";
import SearchBox from "./components/SearchBox"

function App() {
  const[users,setUsers]=useState([])
  const[loading,setLoading]=useState(true)
  const[error,setError]=useState(null)
  const[query,setQuery]=useState("")



  useEffect(()=>{
    async function fetchUsers(){
    try {
      const response = await fetch("https://jsonplaceholder.typicode.com/users")
      const data = await response.json()
      setUsers(data)
      setLoading(false)
    } catch (error) {
      setLoading(false)
      setError("Something went Wrong")
    }
  }
  fetchUsers()
  },[])


  const filteredUsers = users.filter((user) => user.name.toLowerCase().includes(query.toLowerCase()))

  return (    
    <div className="gallery">
      <h1>Gallery</h1>
      <SearchBox query={query} setQuery={setQuery}/>
      <p>{loading? "Loading..............": null}</p>
      <p>{error!=null? error:null}</p>
      
      

      {
      filteredUsers.map((user)=>(
        <UserCard key={user.id} name={user.name} email={user.email}/>
      ))
      }
    </div>
  );
}

export default App;