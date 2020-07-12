import React from "react"

class SearchButton extends React.Component{
  constructor(props){
    this.state{

    }
  }

  const sendIsbn = (bookmeta, rowNum) => {
    this.liff.sendMessages([{
      type: "text",
      text: bookmeta.filter((x, rowNum) => this.state.columnNames[rowNum] === "isbn")[0]
    }])
      .then(() => {
        this.liff.closeWindow()
      })
      .catch((err) => {
        this.setState({
          err: true,
          err_msg: err.message
        })
      })
  }

  render(){
    const button = (
      <button key={colNum} onClick={() => {
        if (this.state.os === "web"){
          alert("Webbrosers cannot use this function")
        }else if (this.liff.isInClient()){
          this.liff.sendMessages([
          {
            type: "text",
            text: bookmeta.filter((x, n) => this.state.columnNames[n] === "isbn")[0]
          }
          ])
            .then(() => {
              liff.closeWindow()
            })
            .catch((err) => {
              document.getElementById("root").textContent = err
            })
        }
      }}>
        Re-search
      </button>
    )
  }

}
