def procesar_archaea_bacteria(archaea):




    """ 
     Toma como parametro un dataframe, y devuelve el dataframe procesado, y lo mismo con OTRAS
       """
    
    archaea['Nombre'] = archaea['index'].apply(lambda x: x.split('__')[-1] if x.split('__')[-1] else 'uncultured')

    # Reemplazar los valores vacíos o nulos con 'uncultured'
    archaea['Nombre'] = archaea['Nombre'].replace('', 'uncultured')
    uncultured_sum = archaea[archaea['Nombre'] == 'uncultured'].sum()

    # Crear una nueva fila para 'uncultured' con los valores sumados y añadir una columna 'Nombre'
    uncultured_row = pd.Series(uncultured_sum, name='uncultured').to_frame().T
    uncultured_row['Nombre'] = 'uncultured'

    # Filtrar el DataFrame original para excluir las filas 'uncultured'
    df_filtered = archaea[archaea['Nombre'] != 'uncultured']

    # Añadir la fila condensada 'uncultured' al DataFrame filtrado
    archaea_final = pd.concat([df_filtered, uncultured_row], ignore_index=True)

    archaea = archaea_final.drop(columns=['index']).set_index('Nombre') # Pone la col Nombre como index
    for column in archaea.columns:
        archaea[f'{column}_relativa'] = archaea[column] / (archaea[column].sum()) *100 # Crea las columnas de abundancias relativas


    lista_cols_filtradas  = [col for col in archaea.columns if '_relativa' in col]

    archaea['max'] = archaea[lista_cols_filtradas].max(axis=1)

    lista_cols_filtradas.append('max')
    archaea=archaea[lista_cols_filtradas].sort_values('max',ascending=False)
    #### hasta aca retunrea lo primero####

    columns_relativa = [col for col in archaea.columns if col.endswith('_relativa')]
    filtered_df = archaea[(archaea[columns_relativa] < 0.5).all(axis=1)]


    # Sumar los valores de las filas filtradas
    otras_sum = filtered_df.sum()

    # Crear una nueva fila con los valores sumados y el nombre 'Otras'
    otras_row = pd.DataFrame([otras_sum], index=['Otras'])

    # Filtrar el DataFrame original para excluir las filas que cumplen con el criterio
    df_filtered = archaea[~(archaea[columns_relativa] < 0.5).all(axis=1)]

    # Añadir la fila 'Otras' al DataFrame filtrado
    df_final = pd.concat([df_filtered, otras_row])
    df_final.drop(columns=['max'],inplace=True)

    df_final['max'] = df_final[columns_relativa].max(axis=1)
    columns_relativa.append('max')
    df_final=df_final[columns_relativa].sort_values('max',ascending=False)

    return(archaea, df_final)


if __name__ == '__main__':
    pass