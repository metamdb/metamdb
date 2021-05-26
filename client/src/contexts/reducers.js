import update from 'immutability-helper';

export const mainReducer = (state, action) => {
  switch (action.type) {
    case "UPLOAD_REACTION_MODEL":
      return {
        ...state,
        isReactionModel: true,
        reactions: action.payload.data.reactions,
        metabolites: action.payload.data.metabolites,
        elements: action.payload.data.elements,
        isFluxModel: action.payload.data.isFluxModel
      };
    case "UPLOAD_FLUX_MODEL":
      return {
        ...state,
        isFluxModel: true,
        reactions: action.payload.data.reactions,
      };
    case "SET_LABELING":
      return {
        ...state,
        labelingData: action.payload,
      };
    case "SET_TRANSITION":
      return {
        ...state,
        atomMappingModel: action.payload.atomMappingModel,
        alerts: state.alerts.push(...action.payload.alerts)
          ? action.payload.alerts
          : [],
      };
    case "DELETE_LABELING_DATA":
      return {
        ...state,
        labelingData: null,
        alerts: [],
      };
    case "DELETE_TRANSITION_DATA":
      return {
        ...state,
        atomMappingModel: null,
        alerts: [],
      };
    case "DELETE_FLUX_MODEL":
      return {
        ...state,
        isFluxModel: false,
        fluxes: null,
        alerts: [],
      };
    case "DELETE_REACTION_MODEL":
      return {
        ...state,
        isReactionModel: false,
        elements: null,
        metabolites: null, 
        reactions: null
      };
    case "UPDATE_ATOM_MAPPING":
      return update(state, {reactions: {[action.payload.rowIndex]: {mappings : {[action.payload.index]: {[action.payload.key]: {$set: action.payload.value}}}}}})
    default:
      return state;
  }
};

export const authReducer = (state, action) => {
  switch (action.type) {
    case "LOGIN":
      localStorage.setItem("token", action.payload.token);
      return {
        id: action.payload.id,
        name: action.payload.name,
        isUser: true,
      };
    case "LOGOUT":
      localStorage.removeItem("token");
      return {
        id: null,
        name: null,
        isUser: false,
      };
    default:
      return state;
  }
};
