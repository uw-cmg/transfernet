from sklearn.model_selection import train_test_split
from transfernet import validate, train, models
from sklearn import datasets
import pandas as pd


def main():

    # Parameters
    save_dir = './outputs'
    target = 'delta_e'
    n_epochs = 1000  # Originally 1000
    batch_size = 32
    lr = 0.0001
    patience = 200
    target = 'MedHouseVal'

    data = datasets.fetch_california_housing(as_frame=True)
    X = data['data']
    y = data['target']

    df = pd.concat([X, y], axis=1)

    y = df[target].values
    X = df.drop(target, axis=1).values

    # Define architecture to use
    model = models.CaliforniaHousingNet(X.shape[1])

    # Split on data we start from (source) to what we transfer to (target)
    splits = train_test_split(X, y, train_size=0.8, random_state=0)
    X_source, X_target, y_source, y_target = splits

    # Split source into train and test
    splits = train_test_split(
                              X_source,
                              y_source,
                              train_size=0.8,
                              random_state=0,
                              )
    X_source_train, X_source_test, y_source_train, y_source_test = splits

    # Split target into train and test
    splits = train_test_split(
                              X_target,
                              y_target,
                              train_size=0.8,
                              random_state=0,
                              )
    X_target_train, X_target_test, y_target_train, y_target_test = splits

    # Validate the method by having explicit test sets
    validate.run(
                 X_source_train,
                 y_source_train,
                 X_source_test,
                 y_source_test,
                 X_target_train,
                 y_target_train,
                 X_target_test,
                 y_target_test,
                 model,
                 n_epochs,
                 batch_size,
                 lr,
                 patience,
                 save_dir,
                 )

    # Train 1 model on all data
    train.run(
              X_source,
              y_source,
              X_target,
              y_target,
              model,
              n_epochs,
              batch_size,
              lr,
              patience,
              save_dir,
              )


if __name__ == '__main__':
    main()
