import React from "react"
import { initializeLiff } from "./liffInit"
import liff from "@line/liff"

class Endpoint extends React.Component{
  constructor(props){
    super(props)
    this.state = ({
      liffId: this.props.liffId
    })
  }

  componentDidMount(){
    initializeLiff(this.state.liffId, ()=>{})
    liff.init()
  }

  render(){
    return (
      <div>
        <h1>endpoint page</h1>
      </div>
    )
  }
}

export default Endpoint
