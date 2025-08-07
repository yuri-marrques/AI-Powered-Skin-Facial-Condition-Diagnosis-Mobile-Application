# flask
from flask import Flask, request, send_file
# cross origins
from flask_cors import CORS, cross_origin
# date and time
from datetime import datetime
from datetime import timedelta
# json 
from flask import jsonify
import json
# to do with file naming structure before saving it
from werkzeug.utils import secure_filename
# database related imports
from database import init_db
from models import User, AccessTokens, Product
# file paths
from pathlib import Path
# password encryption stuff
from encrypt import encrypt_password
from encrypt import check_encrypted_password
# prediction stuff
from classify import classify
# skin data
from skin_data import skin_types, skin_disorders

app = Flask(__name__)
app.debug = True

# Cross Origins Stuff
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'
# app.config['CORS_RESOURCES'] = {r"/*": {"origins": ["http://localhost:3000"]}}
cors = CORS(app)

# current file directory as root
root = Path('.')

# user functions **********************************************************************************

# handle registration
@app.route('/signup', methods=['POST'])
def signup():
    
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password']
    encrypted_password = encrypt_password(password)
    allergic_to = request.form['allergic_to']

    existing_users_with_same_email = User.objects.filter(email = email)

    if len(existing_users_with_same_email) != 0:
        return 'Email already registered'
    else:

        user = User(
            firstname = firstname,
            lastname = lastname,
            email = email,
            password = encrypted_password,
            date_joined = str(datetime.now()),
            verified = True,
            allergic_to = allergic_to
        )
        user.save()

        return 'Signup successful'

# handle login
@app.route('/signin', methods=['POST'])
def signin():
    email = request.form['email']
    password = request.form['password']

    user_verified = User.objects.filter(email = email, verified=True)
    user_not_verified = User.objects.filter(email = email, verified=False)
    
    if len(user_verified) != 0:
        user_encrypted_password = user_verified[0].password
        is_password_entered_true = check_encrypted_password(password, user_encrypted_password)

        if is_password_entered_true == True:
            user_id = user_verified[0].id

            token = AccessTokens(
                user_id = str(user_id),
                active = True,
                signin_date = str(datetime.now())
            )
            token_details = token.save()
            access_token = token_details.id

            return_object = {
                'user_name': user_verified[0].firstname + ' ' + user_verified[0].lastname,
                'status': 'successful',
                'access_token': str(access_token)
            }
            return jsonify(return_object)
        else:
            return_object = {
                'status': 'failed'
            }
            return jsonify(return_object)
    else:
        if len(user_not_verified) != 0:
            user_encrypted_password = user_verified[0].password
            is_password_entered_true = check_encrypted_password(password, user_encrypted_password)

            if is_password_entered_true == True:
                return_object = {
                    'status': 'not verified'
                }
                return jsonify(return_object)
            else:
                return_object = {
                    'status': 'failed'
                }
                return jsonify(return_object)
        else:
            return_object = {
                'status': 'failed'
            }
            return jsonify(return_object)

# get user details by access token issued on sign in
@app.route('/getUserDetailsByAccessToken/<access_token>', methods=['GET'])
def getUserById(access_token):
    try:
        user_id = AccessTokens.objects.filter(id=access_token, active = True)[0].user_id
        user_data = User.objects.filter(id=user_id)[0]
        return user_data.to_json()
    except:
        return 'Not authorized'


# deactivate access token, function is called if user chooses to sign out
@app.route('/deactivateAccessToken/<token>', methods=['GET'])
def deactivateAccessToken(token):
    try:
        AccessTokens.objects(id=token).update(active = False)
        return 'Token deactivated'
    except:
        return 'Invalid token'


# prediction functions *****************************************************************************

# analyze an image
@app.route('/analyzeImage', methods=['POST'])
def analyzeImage():
    user_id = ''
    
    try:
        user_access_token = request.form['user_access_token']
        user_id = AccessTokens.objects.filter(id = user_access_token, active = True)[0].user_id
    except:
        return 'Not authorized'

    # get image base64 from request data
    base64 = request.form['image']

    # get image extension from request data
    extension = request.form['image_extension']

    # save image base64 as decoded image file and return image filename
    from image_base64_to_image_file import image_base64_to_image_file
    image_filename = image_base64_to_image_file(base64, extension)

    # check if image contains a human face or not
    from check_for_human_face import has_face
    contains_face = has_face(image_filename)
    if contains_face == False:
        return 'no human face found'

    # automatically crop image to just the first human face detected
    from crop_image_to_human_face import crop_face
    crop_face(image_filename, save_path=image_filename, margin_ratio=0.3)

    # pass image name to classifier and get prediction results
    predictions, probabilities = classify(image_filename)

    # get skin types and disorders
    skin_type_list = skin_types()
    skin_disorder_list = skin_disorders()

    # loop through predictions to get skin type and skin disorder with highest match probabilities
    skin_type_match = None          # for storing skin type with the highest probability
    skin_type_probability = 0       # for storing probability score for the skin type match
    skin_disorder_match = None      # for storing skin disorder with the highest probability
    skin_disorder_probability = 0   # for storing probability score for the skin disorder match

    # set probability threshold percentange
    probability_threshold = 2

    for i in range(0, len(predictions), +1):
        current_prediction = predictions[i]
        current_probability = probabilities[i]

        # if current probability is >= probability threshold then consider current prediction otherwise disregard it
        if current_probability >= probability_threshold:

            # check if current prediction is a skin type or skin disorder, then execute accordingly
            if current_prediction in skin_type_list:    # is a skin type

                if ((skin_type_probability == 0) or (skin_type_probability < current_probability)):
                    skin_type_match = current_prediction
                    skin_type_probability = current_probability
            
            elif current_prediction in skin_disorder_list:  # is a skin disorder

                if ((skin_disorder_probability == 0) or (skin_disorder_probability < current_probability)):
                    skin_disorder_match = current_prediction
                    skin_disorder_probability = current_probability

    # get all products
    all_products = Product.objects.all()

    # get recommended products, lifestyle
    from skin_data import recommendations
    recommended_products = []
    recommended_routine = {}
    if skin_type_match != None: # if a skin type match was found

        product_recommendation_based_on_skin_type = [item for item in all_products if skin_type_match in item.target_skin_types]
        recommended_products = recommended_products + product_recommendation_based_on_skin_type
        recommended_routine = recommendations(skin_type_match)
        print(
            '\n\n',
            'Skin type with highest match probability:', skin_type_match,'\n',
            'Number of products found based on the skin type:', len(product_recommendation_based_on_skin_type),
            'Recommended routinee:', recommended_routine,
            '\n\n'
        )

    if skin_disorder_match != None: # if a skin disorder match was found

        product_recommendation_based_on_skin_disorder = [item for item in all_products if skin_disorder_match in item.target_skin_disorders]
        recommended_products = recommended_products + product_recommendation_based_on_skin_disorder
        print(
            'Skin disorder with highest match probability:', skin_disorder_match,'\n',
            'Number of products found based on the skin disorder:', len(product_recommendation_based_on_skin_disorder),
            '\n\n'
        )

    # filter products by user allergies
    from allergy_match import allergy_match
    maximum_match_threshold = 0.8 # max = 1, min = 0
    user_details = User.objects.filter(id = user_id)[0]
    user_allergic_to_str = user_details.allergic_to
    user_allergic_to = user_allergic_to_str.lower().split(',')
    print('User allergies:', user_allergic_to, '\n\n')
    recommended_products = [i for i in recommended_products if allergy_match(user_allergic_to, i.allergens.lower().split(',')) < maximum_match_threshold]
    print('Recommended products after filtering by user allergies:', recommended_products, '\n\n')

    # manually recreate recommended products list to stringify mongo ids since we now have a python list with results and not a mongo object, to avoid json errors
    recommended_products_list = []
    for item in recommended_products:

        product_object = {
            '_id': {'$oid': str(item.id)},
            'name': item.name,
            'description': item.description,
            'image': item.image,
            'price': item.price,
            'target_skin_types': item.target_skin_types,
            'target_skin_disorders': item.target_skin_disorders
        }
        recommended_products_list.append(product_object)

    # create results object
    result_object = {
        'skin_type_match': str(skin_type_match),
        'skin_disorder_match': str(skin_disorder_match),
        'recommended_products_list': recommended_products_list,
        'recommended_routine': recommended_routine,
        'user_allergic_to': user_allergic_to_str
    }

    # return recommended products, skin type and skin disorder found to the user
    return jsonify(result_object)



# product functions *********************************************************************************

# add a product
@app.route('/addProduct', methods=['POST'])
def addProduct():
    user_id = ''
    
    # try:
    #     user_access_token = request.form['user_access_token']
    #     user_id = AccessTokens.objects.filter(id = user_access_token, active = True)[0].user_id
    # except:
    #     return 'Not authorized'

    # get expected variables from request data
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    target_skin_types= request.form['target_skin_types']
    target_skin_disorders = request.form['target_skin_disorders']
    allergens = request.form['allergens']

    # get image base64 from request data
    base64 = request.form['image']

    # get image extension from request data
    extension = request.form['image_extension']

    # save image base64 as decoded image file and return image filename
    from image_base64_to_image_file import image_base64_to_image_file
    image_filename = image_base64_to_image_file(base64, extension)

    product_details = Product(
        name = name,
        description = description,
        image = image_filename,
        price = price,
        target_skin_types = target_skin_types,
        target_skin_disorders = target_skin_disorders,
        allergens = allergens
    )

    product_details.save()

    return 'Successful'

# edit product
@app.route('/editProduct', methods=['POST'])
def editProduct():
    user_id = ''
    
    # try:
    #     user_access_token = request.form['user_access_token']
    #     user_id = AccessTokens.objects.filter(id = user_access_token, active = True)[0].user_id
    # except:
    #     return 'Not authorized'

    Product.objects(id = request.form['product_id']).update(name = request.form['name'], price = request.form['price'], description = request.form['description'], allergens = request.form['allergens'])

    return 'Successful'

# delete product
@app.route('/deleteProduct', methods=['POST'])
def deleteProduct():
    user_id = ''
    
    # try:
    #     user_access_token = request.form['user_access_token']
    #     user_id = AccessTokens.objects.filter(id = user_access_token, active = True)[0].user_id
    # except:
    #     return 'Not authorized'

    Product.objects(id = request.form['product_id']).delete()

    return 'Successful'

# view single product
@app.route('/getProduct', methods=['POST'])
def getProduct():

    product_id = request.form['product_id']

    product = Product.objects.filter(id = product_id)[0]

    return product.to_json()

# view all products
@app.route('/getAllProducts', methods=['POST'])
def getAllProducts():

    products = Product.objects.all()

    return products.to_json()

# media retrieval ******************************************************************************

# get media by filename
@app.route('/media/<filename>', methods=['GET', 'POST'])
def media(filename):
    filename = secure_filename(filename)
    filepath = filename
    
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0',threaded = False)