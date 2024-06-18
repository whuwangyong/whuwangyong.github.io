---
title: "为什么jackson databind会调用类里面的一些不相关的public setter方法"
date: 2024-06-18
tags: ["jackson"]
categories: ["springboot"]
---

### 问题

在做spring web开发的时候，发现jackson databind在序列化对象时，会进到一个`getXXX()`方法中，该方法并不是获取类中某个属性的方法。问了ChatGPT-4：

> Jackson使用反射来查找类中的方法和属性。如果类中有符合命名约定的方法（如`getXyz`、`isXyz`），Jackson会尝试调用这些方法。
>
> 如果你不希望某个公共方法被Jackson调用，可以在该方法上添加`@JsonIgnore`注解。

以下是完整回答：

> 在使用 Jackson 数据绑定（databind）进行 JSON 序列化和反序列化时，你可能会遇到它调用类中的一些公共方法。以下是一些可能导致这种行为的原因和解决方案：
>
> ### 可能原因
>
> 1. **getter方法**:
>
>     * Jackson默认会调用类中的公共getter方法来获取属性值以进行序列化。例如，如果你有一个名为`getSomething`的方法，Jackson会认为这是一个属性的getter方法，并尝试调用它。
> 2. **​`@JsonProperty`​**​**注解**:
>
>     * 如果你在一个公共方法上使用了`@JsonProperty`注解，Jackson会使用该方法作为一个属性的getter或setter方法。
> 3. **​`@JsonGetter`​**​**和**​ **​`@JsonSetter`​**​**注解**:
>
>     * 这些注解可以显式地告诉Jackson将某个方法作为getter或setter方法进行序列化或反序列化。
> 4. **默认构造函数和工厂方法**:
>
>     * Jackson在反序列化时需要一个无参构造函数来创建对象。如果你有一个静态工厂方法并且标注了`@JsonCreator`，Jackson也会调用它来创建实例。
> 5. **反射**:
>
>     * Jackson使用反射来查找类中的方法和属性。如果类中有符合命名约定的方法（如`getXyz`、`isXyz`），Jackson会尝试调用这些方法。
>
> ### 解决方案
>
> 1. **使用**​ **​`@JsonIgnore`​**​**注解**:
>
>     * 如果你不希望某个公共方法被Jackson调用，可以在该方法上添加`@JsonIgnore`注解。
>
>     ```java
>     public class MyClass {
>         @JsonIgnore
>         public void someUnrelatedMethod() {
>             // This method will be ignored by Jackson
>         }
>     }
>     ```
> 2. **自定义序列化和反序列化逻辑**:
>
>     * 如果你需要更精细地控制序列化和反序列化过程，可以自定义序列化器和反序列化器。
>
>     ```java
>     public class MyClassSerializer extends JsonSerializer<MyClass> {
>         @Override
>         public void serialize(MyClass value, JsonGenerator gen, SerializerProvider serializers) throws IOException {
>             // Custom serialization logic
>         }
>     }
>
>     public class MyClassDeserializer extends JsonDeserializer<MyClass> {
>         @Override
>         public MyClass deserialize(JsonParser p, DeserializationContext ctxt) throws IOException {
>             // Custom deserialization logic
>             return new MyClass();
>         }
>     }
>
>     @JsonSerialize(using = MyClassSerializer.class)
>     @JsonDeserialize(using = MyClassDeserializer.class)
>     public class MyClass {
>         // Class content
>     }
>     ```
> 3. **使用**​**​`ObjectMapper`​**​**配置**:
>
>     * 你可以通过配置`ObjectMapper`来改变默认的行为。
>
>     ```java
>     ObjectMapper mapper = new ObjectMapper();
>     mapper.configure(SerializationFeature.FAIL_ON_EMPTY_BEANS, false);
>     ```
> 4. **避免无关的公共方法**:
>
>     * 重新设计类，避免定义与序列化无关的公共方法，或将这些方法设为私有或受保护的。
>
> ### 示例
>
> 假设有如下类：
>
> ```java
> public class Person {
>     private String name;
>     private int age;
>
>     public String getName() {
>         return name;
>     }
>
>     public void setName(String name) {
>         this.name = name;
>     }
>
>     public int getAge() {
>         return age;
>     }
>
>     public void setAge(int age) {
>         this.age = age;
>     }
>
>     public void someUnrelatedMethod() {
>         // Some unrelated logic
>     }
> }
> ```
>
> 在默认情况下，Jackson会调用`getName`和`getAge`方法，因为这些是标准的getter方法。如果你不希望Jackson调用`someUnrelatedMethod`，可以这样修改：
>
> ```java
> public class Person {
>     private String name;
>     private int age;
>
>     public String getName() {
>         return name;
>     }
>
>     public void setName(String name) {
>         this.name = name;
>     }
>
>     public int getAge() {
>         return age;
>     }
>
>     public void setAge(int age) {
>         this.age = age;
>     }
>
>     @JsonIgnore
>     public void someUnrelatedMethod() {
>         // Some unrelated logic
>     }
> }
> ```
>
> 通过上述方法，你可以更好地控制Jackson在序列化和反序列化过程中调用哪些方法，从而避免调用不相关的方法。

也问了百度文心一言3.5，回答未指出关键：

> Jackson Databind（以及一般的JSON序列化/反序列化库）在处理Java对象时，通常只会关注与JSON结构直接相关的字段和方法，比如类的属性（字段）和getter/setter方法。然而，在某些情况下，Jackson可能会调用其他不直接相关的public方法，这通常是由于以下几个原因：
>
> 1. **自定义序列化/反序列化器**：
>     如果你为某个类定义了自定义的序列化器或反序列化器，并在其中调用了类的其他public方法，那么Jackson在序列化/反序列化过程中就会执行这些方法。
> 2.  **​`@JsonAnyGetter`​** **和**  **​`@JsonAnySetter`​** **注解**：
>     这两个注解允许你定义用于处理JSON中额外字段的方法。例如，`@JsonAnyGetter` 通常与返回一个Map的方法一起使用，该方法提供了对类中未明确映射到JSON字段的属性的访问。同样，`@JsonAnySetter` 通常与接受两个参数（一个键和一个值）的方法一起使用，用于处理JSON中未明确映射的字段。
> 3.  **​`@JsonCreator`​** **注解**：
>     当使用`@JsonCreator`注解的方法作为反序列化构造函数时，Jackson会调用该方法，并传递JSON中的值作为参数。这个方法可能会间接地调用类的其他public方法。
> 4.  **​`@JsonProperty`​** **和**  **​`@JsonIgnore`​** **注解**：
>     虽然这些注解主要用于字段和getter/setter方法，但它们也可以用于其他方法。如果Jackson发现某个方法上有这些注解，它可能会尝试调用该方法。然而，这通常不是推荐的做法，因为可能会导致意外的行为。
> 5.  **​`@JsonSerialize`​** **和**  **​`@JsonDeserialize`​** **注解**：
>     这些注解允许你指定用于序列化/反序列化特定字段或类型的自定义序列化器/反序列化器。如果这些自定义序列化器/反序列化器调用了类的其他public方法，那么Jackson就会执行这些方法。
> 6. **Jackson的延迟引用解析**：
>     在某些情况下，Jackson可能需要延迟解析JSON中的引用（例如，当处理具有循环引用的对象图时）。这可能会导致在序列化/反序列化过程的后期阶段调用类的public方法。
> 7. **Jackson的扩展点和插件**：
>     Jackson提供了许多扩展点和插件机制，允许你自定义其行为。如果你使用了这些扩展点或插件，并且它们调用了类的public方法，那么Jackson就会执行这些方法。
> 8. **类继承和多态**：
>     如果你的类是从其他类继承的，或者使用了多态（例如，在集合中存储了不同类型的对象），那么Jackson可能会调用基类或接口中的public方法。
> 9. **Jackson的bug或不当使用**：
>     在某些情况下，Jackson的行为可能不符合预期，或者你可能以不当的方式使用了Jackson。这可能会导致Jackson调用不相关的public方法。如果你怀疑这是问题的原因，请检查你的代码和Jackson的配置，并考虑升级到最新版本的Jackson。
>
> 为了避免Jackson调用不相关的public方法，你应该仔细审查你的代码和Jackson的配置，确保你只使用了与JSON序列化/反序列化直接相关的字段和方法。同时，注意遵循Jackson的最佳实践和文档中的建议。