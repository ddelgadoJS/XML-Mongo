//////////////////////// MAP REDUCE ALGORITHM ////////////////////////
//////////////////////////////////////////////////////////////////////
// Usar el mecanismo de mapReduce para contar la frecuencia de cada valor del campo PLACES
//////////////////////////////////////////////////////////////////////

db.Kevin1.mapReduce(

  function (){
    var ciudades = this.PLACES
    if (ciudades == null) {
        emit("NULL", 1);
    }
    else{
      if (ciudades.constructor === Array) {
        for (var i = 0; i < ciudades.length; i++) {
          emit(ciudades[i], 1);
        }
      }
      else {
        emit(ciudades, 1);
      }
    }
  },

  function(keys,values){
    return Array.sum(values);
  },

  {out:"map_reduce_result"}

);

db.map_reduce_result.find();


///////////////////////////////// INDEX /////////////////////////////////
/////////////////////////////////////////////////////////////////////////
// Se deben crear los siguientes índices para facilitar el acceso a la información cargada.
// •	Crear un índice ascendente para cada uno de los campos de arreglos (TOPICS, PLACES, PEOPLE, ORGS y EXCHANGES).
// •	Crear un índice de texto para los campos TITLE y BODY.
/////////////////////////////////////////////////////////////////////////

db.Kevin1.createIndex({"TOPICS":1});
db.Kevin1.createIndex({"PLACES":1});
db.Kevin1.createIndex({"PEOPLE":1});
db.Kevin1.createIndex({"ORGS":1});
db.Kevin1.createIndex({"EXCHANGES":1});

db.Kevin1.createIndex({TITLE: "text",
                     BODY: "text"});
