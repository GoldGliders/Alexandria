import React from "react"
import { initializeLiff } from "./liffInit"
import MultiButton from "./multibutton"
import liff from "@line/liff"
import Card from "@material-ui/core/Card"
import CardActions from "@material-ui/core/CardActions"
import CardContent from "@material-ui/core/CardContent"
import CardMedia from "@material-ui/core/CardMedia"
import Grid from "@material-ui/core/Grid"
import Typography from "@material-ui/core/Typography"
import { withStyles } from "@material-ui/core/styles"

const HEIGHT = 75
const useStyles = ((theme) => ({
  root: {
    flexGrow: 1,
  },
  card: {
    height: HEIGHT,
    width: 300,
  },
  textarea: {
  },
  text: {
  },
  button: {
    position: "absolute",
    padding: 0,
    marginLeft: "220px !important",
  }
}))

class LibraryTable extends React.Component{
  constructor(props){
    super(props)
    this.state = {
      timestamps: [],
      libraries: [],
      uri: this.props.uri,
      columnNames: this.props.columnNames,
      liffId: this.props.liffId,
      os: null,
      error: null,
      error_msg: null
    }
    this.getResource = this.getResource.bind(this)
    this.convertTimestamp = this.convertTimestamp.bind(this)
    this.row = this.row.bind(this)
  }

  componentDidMount(){
    initializeLiff(this.state.liffId, this.getResource)
  }

  getResource(resp){
    if (resp["status"] === "ok"){
      fetch(`/api/${this.state.uri}?idToken=${resp["idToken"]}`)
        .then(res => res.json())
        .then((res) => {
          const rows = res["items"].map(item => this.state.columnNames.map(key => item[key]))

          this.setState({
            timestamps: null,
            libraries: rows,
            os: resp["os"],
            error: false
          })
        })
        .catch((err) => {
          this.setState({
            timestamps: null,
            libraries: null,
            error: true,
            error_msg: err.message
          })
          liff.logout()
        })
    }else{
      this.setState({
        timestamps: null,
        libraries: null,
        error: true,
        error_msg: 503
      })
      liff.logout()
    }
  }


  convertTimestamp(colNum, cell){
    if (this.state.columnNames.indexOf("timestamp") === colNum){
      const converted = new Date(cell*1000).toLocaleDateString()
      return converted
    }else{
      return cell
    }
  }

  row(classes){
    const rows = this.state.libraries.map((library, rowNum) => {

      const metadata = (name) => library[this.state.columnNames.indexOf(name)]
      const timestamp = new Date(metadata("timestamp")*1000).toLocaleDateString()
      const formal = metadata("formal")
      const libid = metadata("libid")

      return (
        <Grid container justify="center" alignItems="center" key={rowNum} item xs={12} sm={6} md={4} lg={3} zeroMinWidth>
          <Card variant="outlined" className={classes.card}>
            <CardActions>
              <CardContent className={classes.textarea}>
                <Typography color="textPrimary" variant="body1" component="h2" className={classes.text}>
                  {formal}
                </Typography>
                {/*
                <Grid>
                  <Typography color="textSecondary" variant="body1" component="h2" className={classes.text}>
                    {timestamp}
                  </Typography>
                </Grid>
              </Grid>
            <div className={classes.button}>
              <MultiButton funcName="library" text="remove" formal={formal} libid={libid} idToken={liff.getIDToken()} />
            </div>
            */}
              </CardContent>
              <CardActions className={classes.button}>
                <MultiButton funcName="library" text="remove" formal={formal} libid={libid} idToken={liff.getIDToken()} />
              </CardActions>
            </CardActions>
          </Card>
        </Grid>
      )})

    return rows
  }

  render(){
    const {classes} = this.props

    if (this.state.error){
      return(
        <div>
          <h1>{this.state.error_msg}</h1>
        </div>
      )
    }else{
      return(
        <div className={classes.root}>
          <Grid container spacing={1}>
            {this.row(classes)}
          </Grid>
        </div>
      )
    }
  }
}

export default withStyles(useStyles, {withTheme: true})(LibraryTable)
