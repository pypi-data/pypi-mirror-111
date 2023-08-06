import torch
from torch import nn
import pandas as pd
import matplotlib.pyplot as plt
from msdlib import msd
import numpy as np
import os
import joblib
plt.rcParams['figure.facecolor'] = 'white'


class NNmodel(nn.Module):
    """
    layer_funcs: list, contains sequential layer classes (nn.Module). For example-
                    [nn.Linear(50), nn.ReLU(), nn.Linear(3), nn.Softmax(dim=-1)]
    seed_value: float/int, random seed for reproducibility
    """
    def __init__(self, layer_funcs, seed_value=1216):
        
        super(NNmodel, self).__init__()
        # reproducibility parameters
        np.random.seed(seed_value)
        torch.manual_seed(seed_value)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        
        self.layers = nn.ModuleList(layer_funcs)
        
    def forward(self, x):
        """
        pytorch forward function for forward propagation
        """
        for layer in self.layers:
            x = layer(x)
        return x
    

# The class can be used for auto-encoder architecture
class AutoEncoderModel(nn.Module):
    """
    enc_layers: python list, containing the encoder layers (torch.nn.Module class objects) sequentially
    dec_layers: python list, containing the decoder layers (torch.nn.Module class objects) sequentially
    seed_value: float/int, random seed for reproducibility
    """
    def __init__(self, enc_layers, dec_layers, seed_value=1216):
        
        super(AutoEncoderModel, self).__init__()
        # reproducibility parameters
        np.random.seed(seed_value)
        torch.manual_seed(seed_value)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        
        self.encode_layers = nn.ModuleList(enc_layers)
        self.decode_layers = nn.ModuleList(dec_layers)
        self.enc_len = len(self.encode_layers)
        self.dec_len = len(self.decode_layers)
    
    def encode(self, x):
        """
        Encoder part in Autoencoder model
        x: input tensor for encoder part
        """
        for layer in self.encode_layers:
            x = layer(x)
        return x
    
    def decode(self, x):
        """
        Decoder part in Autoencoder model
        x: input tensor for decoder part
        """
        for layer in self.decode_layers:
            x = layer(x)
        return x
        
    def forward(self, x):
        """
        pytorch forward function for forward propagation, applies encoder and then decoder sequentially on the input data
        x: input tensor for autoencoder model 
        """
        x = self.encode(x)
        x = self.decode(x)
        return x


# torchModel is a scikit like wrapper for pytorch which enables us to use the model for 
# training, predicting and evaluating performance using simple fit, predict and evaluate methods
class torchModel():
    """
    layers: a list of torch.nn.Module objects indicating layers/activation functions. The list should contain all elements sequentially
    loss_func: loss function for the ML model. default is torch.nn.MSELoss. It can also be a custom loss function, but should be equivalent to the default
    optimizer: optimizer for the ML model. default is torch.optim.Adam
    learning_rate: learning rate of the training steps, default is .0001
    epoch: number of epoch for training, default is 2
    batch_size: mini-batch size for trianing, default is 32
    lr_reduce: learning rate reduction base for lambda reduction scheduler from pytorch. (follows torch.optim.lr_scheduler.LambdaLR)
    loss_reduction: loss reduction parameter for loss calculation, default is 'mean'
    model_type: type of the model depending on the objective, available is any of {'regressor', 'classifier'}, default is 'regressor'
    use_gpu: bool, whether to use gpu or not, default is True
    model_name: str, name of the model, default is 'pytorch'
    dtype: dtype of processing inside the model, default is torch.float32
    plot_loss: bool, whether to plot loss curves after training or not, default is True
    quant_perc: float, quantile value to limit the loss values for loss curves, default is .98
    plot_true_pred: bool, whether to plot true-vs-prediction curve or not. For model_type=classifier, it will be score matrix plot and for model_type=regressor, it will be a true vs prediction scatter plot, default is True
    loss_roll_preiod: rolling/moving average period for loss curve
    model: torch.nn.Module class (ML model class), so that you are able to write the model yourself and use fit, predict etc from here.  
    """
    def __init__(self, layers=[], loss_func=None, optimizer=None, learning_rate=.0001, epoch=2, batch_size=32, lr_reduce=1, 
                 loss_reduction='mean', model_type='regressor', use_gpu=True, model_name='pytorch', dtype=torch.float32,
                 plot_loss=True, quant_perc=.98, plot_true_pred=True, loss_roll_period=1, model=None):
        
        # defining model architecture
        self.model = NNmodel(layers) if model is None else model
        self.loss_func = loss_func if loss_func is not None else nn.MSELoss
        self.optimizer = optimizer if optimizer is not None else torch.optim.Adam
        
        # defining training formation parameters
        self.learning_rate = learning_rate
        self.epoch = epoch
        self.batch_size = batch_size
        self.lr_reduce = lr_reduce
        self.loss_reduction = loss_reduction
        self.model_type = model_type
        self.use_gpu = use_gpu
        self.model_name = model_name
        self.dtype = dtype
        
        # evaluation parameters
        self.plot_loss = plot_loss
        self.quant_perc = quant_perc
        self.plot_true_pred = plot_true_pred
        self.loss_roll_period = loss_roll_period
        
        # setting up
        self.device = torch.device("cuda" if self.use_gpu and torch.cuda.is_available() else "cpu")
        self.model = self.model.to(device=self.device, dtype=self.dtype)
        self.loss_func = loss_func(reduction=self.loss_reduction).to(device=self.device, dtype=self.dtype)
        self.optimizer = self.optimizer(self.model.parameters(), lr = self.learning_rate)
        
        # learning rate scheduler
        lr_lambda = lambda ep : self.lr_reduce ** ep
        self.scheduler = torch.optim.lr_scheduler.LambdaLR(self.optimizer, lr_lambda)
        
    
    def fit(self, data, label, validation_ratio=.15, evaluate=True, figsize=(18, 4)):
        """
        scikit like wrapper for training DNN pytorch model
        data: input train data, must be torch tensor or numpy ndarray
        label: supervised labels for data, must be torch tensor or numpy ndarray
        validation_ratio: ratio of 'data' that will be used for validation during training
        """
        
        # allowing pandas dataframe or series input
        if isinstance(data, pd.DataFrame): data = data.values
        elif isinstance(data, pd.Series): data = data.to_frame().values
        if isinstance(label, pd.DataFrame): label = label.values
        elif isinstance(label, pd.Series): label = label.values
        
        # splitting data set
        train_ratio = 1 - validation_ratio
        idx = np.arange(label.shape[0])
        np.random.shuffle(idx)
        train_idx = idx[:int(train_ratio * label.shape[0])]
        val_idx = idx[int(train_ratio * label.shape[0]):]
        
        # getting the model and data ready
        total_batch = train_idx.shape[0] // self.batch_size + int(bool(train_idx.shape[0] % self.batch_size))
        
        train_data = data[train_idx]
        train_label = label[train_idx]
        val_data = data[val_idx]
        val_label = label[val_idx]
        
        # handling data sets and labels
        if not isinstance(train_data, torch.Tensor): train_data = torch.from_numpy(train_data)
        if not isinstance(val_data, torch.Tensor): val_data = torch.from_numpy(val_data)
        if not isinstance(train_label, torch.Tensor): train_label = torch.from_numpy(train_label)
        if not isinstance(val_label, torch.Tensor): val_label = torch.from_numpy(val_label)
        
        # data type conversion
        train_data = train_data.to(device=self.device, dtype=self.dtype)
        train_label = train_label.to(device=self.device, dtype=self.dtype) if self.model_type.lower() == 'regressor' else train_label.to(device=self.device, dtype=torch.long)
        val_data = val_data.to(device=self.device, dtype=self.dtype)
        val_label = val_label.to(device=self.device, dtype=self.dtype) if self.model_type.lower() == 'regressor' else val_label.to(device=self.device, dtype=torch.long)
        
        # running through epoch
        loss_curves = [[], []]
        val_loss = torch.tensor(np.nan)
        for ep in range(self.epoch):
            tr_mean_loss = []
            self.model.train()
            for i in range(total_batch):
                # preparing data set
                if i != total_batch - 1:
                    batch_data = train_data[i * self.batch_size : (i + 1) * self.batch_size]
                    batch_label = train_label[i * self.batch_size : (i + 1) * self.batch_size]
                else:
                    batch_data = train_data[-self.batch_size:]
                    batch_label = train_label[-self.batch_size:]
                
                # loss calculation
                self.model.zero_grad()
                label_hat = self.model(batch_data).squeeze()
                tr_loss = self.loss_func(label_hat, batch_label)
                
                # back-propagation
                tr_loss.backward()
                # model parameter update
                self.optimizer.step()
                
                # stacking and printing losses
                tr_mean_loss.append(tr_loss.item())
                print('\repoch : %04d/%04d, batch : %03d, train_loss : %.4f, validation_loss : %.4f,            '
                      % (ep + 1, self.epoch, i + 1, tr_loss.item(), val_loss.item()), end = '')
            
            # loss scheduler step
            self.scheduler.step()
            # storing losses
            loss_curves[0].append(np.mean(tr_mean_loss))
            
            if val_data.shape[0] > 0:
                # run evaluation to get validation score
                self.model.eval()
                out = self.predict(val_data).squeeze()
                val_loss = self.loss_func(out, val_label)
                # storing losses
                loss_curves[1].append(val_loss.item())
        
        print('...training complete !!')
        losses = pd.DataFrame(loss_curves, index = ['train_loss', 'validation_loss'], columns = np.arange(1, self.epoch + 1)).T.rolling(self.loss_roll_period).mean()
        
        # plotting loss curve
        if self.plot_loss and self.epoch > 1:
            ylim_upper = losses.quantile(self.quant_perc).max()
            ylim_lower = losses.min().min()
            fig, ax = plt.subplots(figsize = (25, 4))
            losses.plot(ax = ax, color = ['darkcyan', 'crimson'])
            ax.set_ylim(ylim_lower, ylim_upper)
            fig.suptitle('Learning curves', y = 1, fontsize = 15, fontweight = 'bold')
            fig.tight_layout()
            plt.show()

        # model training evaluation
        if evaluate: self.evaluate([train_data, val_data], [train_label, val_label], set_names=['Train_set', 'Validation_set'], figsize=figsize)



    def predict(self, data):
        """
        a wrapper function that generates prediction from pytorch model
        data: input data to predict on, must be a torch tensor or numpy ndarray
        returns predictions
        """
        
        # checking data type
        if isinstance(data, pd.DataFrame) or isinstance(data, pd.Series): data = data.values
        if isinstance(data, np.ndarray): data = torch.from_numpy(data)
        data = data.to(device=self.device, dtype=self.dtype)
        
        # estimating number of mini-batch
        n_batch = data.shape[0] // self.batch_size + int(bool(data.shape[0] % self.batch_size))
        # generates prediction
        preds = []
        for i in range(n_batch):
            if i != n_batch - 1:
                pred = self.model(data[i * self.batch_size: (i + 1) * self.batch_size])
            else:
                pred = self.model(data[i * self.batch_size:])
            preds.append(pred.detach())
        preds = torch.cat(preds)
        return preds
    
    
    def evaluate(self, data_sets, label_sets, set_names=[], figsize=(18, 4)):
        """
        a customized function to evaluate model performance in regression and classification type tasks
        data_sets: list of data, data must be nunmpy ndarray or torch tensor
        label_sets: list of labels corresponding to each data, label must be nunmpy ndarray or torch tensor
        set_names: names of the data sets
        figsize: figure size for the evaluation plots
        """

        results, all_results = None, None
        # plotting true vs prediction curve (regression) or confusion matrix (classification)
        if self.plot_true_pred and self.model_type.lower() in ['regressor', 'classifier'] and len(data_sets) > 0:
            set_names = set_names if len(set_names) > 0 else ['data-%d'%(i+1) for i in range(len(data_sets))]
            all_results = {}
            results = []
            self.model.eval()
            for i, (preddata, predlabel) in enumerate(zip(data_sets, label_sets)):
                test_pred = self.predict(preddata).detach().cpu().squeeze().numpy()
                label = predlabel.detach().cpu().squeeze().numpy()
                if self.model_type.lower() == 'regressor':
                    true_pred = pd.DataFrame([label, test_pred], index = ['true_label', 'prediction']).T
                    corr_val = true_pred.corr().iloc[0, 1]
                    rsquare, rmse = msd.rsquare_rmse(true_pred['true_label'].values, true_pred['prediction'].values)
                    fig, ax = plt.subplots(figsize=figsize)
                    ax.scatter(true_pred['true_label'], true_pred['prediction'], color = 'darkcyan', s = 8)
                    _min = np.min([true_pred['true_label'].min(), true_pred['prediction'].min()])
                    _max = np.max([true_pred['true_label'].max(), true_pred['prediction'].max()])
                    ax.plot([_min, _max], [_min, _max], color='k', lw=2)
                    print(_min, _max)
                    ax.set_xlabel('true-label')
                    ax.set_ylabel('prediction')
                    ax.set_title('True-Label VS Prediction Scatter plot for %s from %s\nRSquare : %.3f,  RMSE : %.3f,  Correlation : %.3f'
                                 %(set_names[i], self.model_name, rsquare, rmse, corr_val))
                    all_results[set_names[i]] = [rsquare, rmse]
                    results.append(pd.Series([rsquare, rmse], index = ['r_square', 'rmse'], name = '%s_%s'%(self.model_name, set_names[i])))
                elif self.model_type.lower() == 'classifier':
                    test_pred = np.argmax(test_pred, axis=1)
                    result, confus = msd.class_result(label, test_pred, out_confus = True)
                    fig, ax = plt.subplots(figsize=figsize, ncols = 2)
                    ax[0] = msd.plot_heatmap(result, annotate = True, fmt = '.3f', xrot = 0, vmax = 1, axobj = ax[0], cmap = 'summer', fig_title = 'Score Matrix')
                    ax[1] = msd.plot_heatmap(confus, annotate = True, fmt = 'd', xrot = 0, axobj = ax[1], cmap = 'Blues', fig_title = 'Confusion Matrix')
                    fig.suptitle('Classification result for %s from %s'%(set_names[i], self.model_name), fontsize = 15, fontweight = 'bold')
                    all_results[set_names[i]] = [result, confus]
                    results.append(pd.Series(result.mean().drop('average').to_list() + [result['average'].loc['accuracy']], index = result.drop('average', axis = 1).columns.to_list() + ['average'], 
                                             name = '%s_%s'%(self.model_name, set_names[i])))
                fig.tight_layout()
                plt.show()
            results = pd.concat(results, axis = 1, sort = False).T

        return results, all_results


def get_factors(n_layers, base_factor=5, max_factor=10, offset_factor=2):
    """
    n_layers: number of hidden layers
    offset_factor: makes assymetric structure (base - offset)
    max_factor: multiplier for mid layer (largest layer)
    base_factor: multiplier for first layer
    """
    base_factor = max_factor - base_factor
    return [max_factor - abs(x) for x in np.linspace(-base_factor, base_factor + offset_factor, n_layers) if max_factor - abs(x) > 0]



def define_layers(input_units, output_units, unit_factors, dropout_rate, model_type, actual_units=False):
    """
    input_units: int, number of units in input layer / number of features (not first hidden layer)
    output_units: int, number of units in output layer / number of output nodes / number of classes (not last hidden layer)
    unit_factors: array of ints or floats, multipliers to calculate number of units in each hidden layer from input_units, or actual number of units for each hidden layer
    dropout_rate: dropout ratio
    model_type: {'classifier', 'regressor'}, controls use of softmax on top of output layer
    actual_units: bool, whether actual units are placed in unit_factors or not
    """
    if actual_units:
        hidden_units = unit_factors.copy()
    else:
        hidden_units = [input_units * factor for factor in unit_factors]
    units = [input_units] + hidden_units + [output_units]
    units = [int(i) for i in units]
    
    layers = []
    for i in range(len(unit_factors)):
        layers.append(nn.Linear(units[i], units[i + 1]))
        layers.append(nn.BatchNorm1d(units[i + 1]))
        layers.append(nn.ReLU())
        layers.append(nn.Dropout(dropout_rate))
    layers.append(nn.Linear(units[-2], units[-1]))
    if model_type == 'classifier':
        layers.append(nn.Softmax(dim=1))
    return layers


# storing the models and loading them
def store_models(models, folder_path):
    """
    models: dict, containing only trained model class; {<model name>: <model class>}
            For pytorch models, the key must contain 'pytorch' phrase
    folder_path: str, the folder path where the models will be stores, if doesnt exist, it will be created
    """
    if not os.path.exists(folder_path): os.makedirs(folder_path)
    for modelname in models:
        print('storing models... %s_model...'%modelname, end='')
        if 'pytorch' in modelname.lower():
            torch.save(models[modelname].model.state_dict(), folder_path + '/%s_model.pt'%modelname)
        else:
            with open(folder_path + '/%s_model.pickle'%modelname, 'wb') as f:
                joblib.dump(models[modelname], f)
        print('   ...storing completed !!')
    

def load_models(models, folder_path):
    """
    models: dict, containing model classes or None (for torch model, pytorch nn.Module class is necessary 
            to load the state variables. For other types of models like xgboost etc. None is fine.);
            For pytorch models, the key must contain 'pytorch' phrase
            key name must be like this :
            stored model file name: xgboost_model.pickle
            corresponding key for the dict: 'xgboost'
    folder_path: str, folder path from where the stored models will be loaded
    """
    for modelname in models:
        print('\rloading models... %s_model...'%modelname, end='')
        if 'pytorch' in modelname.lower():
            models[modelname].model.load_state_dict(torch.load(folder_path + '/%s_model.pt'%modelname))
        else:
            with open(folder_path + '%s_model.pickle'%modelname, 'rb') as f:
                models[modelname] = joblib.load(f)
        print('   ...loading completed !!')
    return models

